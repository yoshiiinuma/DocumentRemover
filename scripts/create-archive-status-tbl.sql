DELIMITER $$

DROP PROCEDURE IF EXISTS CreateArchiveStatus;

CREATE PROCEDURE CreateArchiveStatus(IN days1 INT, IN days2 INT)
BEGIN
  DECLARE days3 INT;
  DECLARE days4 INT;

  SET days1 = IFNULL(days1, 60);
  SET days2 = IFNULL(days2, 240);
  SET days3 = days1 + 30;
  SET days4 = days2 + 30;

  DROP TEMPORARY TABLE IF EXISTS ArchiveStatus;

  CREATE TEMPORARY TABLE ArchiveStatus
  (
    TargetDate DATE,
    ArchiveDate DATE,
    DeleteDate DATE,
    Cnt INT,
    ArchiveType TINYINT 
  );

  DROP TEMPORARY TABLE IF EXISTS ArchiveSummary;

  CREATE TEMPORARY TABLE ArchiveSummary
  (
    ArchiveDate DATE,
    DeleteDate DATE,
    Cnt INT
  );

  INSERT INTO ArchiveStatus (TargetDate, ArchiveDAte, DeleteDate, Cnt, ArchiveType)
  SELECT LastDate, LastDate + INTERVAL days1 DAY, LastDate + INTERVAL days3 DAY, COUNT(*), 1
    FROM Requests r
    LEFT JOIN (
           SELECT RequestId, DATE(MAX(`Arrival Date`)) AS LastDate
             FROM Travelers
            GROUP BY RequestId) AS t
      ON t.RequestId = r.RequestId
   WHERE (Archived = 0 OR Archived = NULL)
     AND Status IN ('Approved', 'Denied', 'Other Resolution', 'Admin Close')
     AND LastDate IS NOT NULL
     AND DATEDIFF(LastDate, DATE(r.CreatedAt)) >= -10
     AND DATEDIFF(LastDate, DATE(r.CreatedAt)) <= 180
   GROUP BY LastDate
   ORDER BY LastDate;

  INSERT INTO ArchiveStatus (TargetDate, ArchiveDate, DeleteDate, Cnt, ArchiveType)
  SELECT DATE(r.UpdatedAt) AS LastUpdate, MAX(DATE(r.UpdatedAt) + INTERVAL days2 DAY),
         MAX(DATE(r.UpdatedAt) + INTERVAL days4 DAY), COUNT(*), 2
    FROM Requests r
    LEFT JOIN (
           SELECT RequestId, DATE(MAX(`Arrival Date`)) AS LastDate
             FROM Travelers
            GROUP BY RequestId) AS t
      ON t.RequestId = r.RequestId
   WHERE (Archived = 0 OR Archived = NULL)
     AND Status IN ('Approved', 'Denied', 'Other Resolution', 'Admin Close')
     AND (LastDate IS NULL
          OR DATEDIFF(LastDate, DATE(r.CreatedAt)) < -10
          OR DATEDIFF(LastDate, DATE(r.CreatedAt)) > 180)
   GROUP BY DATE(r.UpdatedAt)
   ORDER BY DATE(r.UpdatedAt);

  INSERT INTO ArchiveSummary (ArchiveDate, DeleteDate, Cnt)
  SELECT ArchiveDate, DeleteDate, SUM(Cnt)
    FROM ArchiveStatus
   GROUP BY ArchiveDate, DeleteDate;

END$$

DELIMITER ;
