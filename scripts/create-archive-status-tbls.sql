DELIMITER $$

DROP PROCEDURE IF EXISTS CreateArchiveDateCount;

CREATE PROCEDURE CreateArchiveDateCount(IN days1 INT, IN days2 INT, IN days3 INT)
BEGIN
  SET days1 = IFNULL(days1 + 1, 61);
  SET days2 = IFNULL(days2 + 1, 241);
  SET days3 = IFNULL(days3, 30);

  DROP TEMPORARY TABLE IF EXISTS ArchiveDateCount;

  CREATE TEMPORARY TABLE ArchiveDateCount
  (
    TargetDate DATE,
    ArchiveDate DATE,
    DeleteDate DATE,
    RequestCount INT,
    ArchiveType TINYINT 
  );

  DROP TEMPORARY TABLE IF EXISTS ArchiveDateSummary;

  CREATE TEMPORARY TABLE ArchiveDateSummary
  (
    ArchiveDate DATE,
    DeleteDate DATE,
    RequestCount INT
  );

  INSERT INTO ArchiveDateCount (TargetDate, ArchiveDate, DeleteDate, RequestCount, ArchiveType)
  SELECT LastDate, LastDate + INTERVAL days1 DAY,
         LastDate + INTERVAL days1 + days3 DAY, COUNT(*), 1
    FROM Requests r
    LEFT JOIN (
           SELECT RequestId, DATE(MAX(`Arrival Date`)) AS LastDate
             FROM Travelers
            GROUP BY RequestId) AS t
      ON t.RequestId = r.RequestId
   WHERE Status IN ('Approved', 'Denied', 'Other Resolution', 'Admin Close')
     AND LastDate IS NOT NULL
     AND DATEDIFF(LastDate, DATE(r.CreatedAt)) >= -10
     AND DATEDIFF(LastDate, DATE(r.CreatedAt)) <= 180
   GROUP BY LastDate
   ORDER BY LastDate;

  INSERT INTO ArchiveDateCount (TargetDate, ArchiveDate, DeleteDate, RequestCount, ArchiveType)
  SELECT DATE(r.UpdatedAt) AS LastUpdate, MAX(DATE(r.UpdatedAt) + INTERVAL days2 DAY),
         MAX(DATE(r.UpdatedAt) + INTERVAL days2 + days3 DAY), COUNT(*), 2
    FROM Requests r
    LEFT JOIN (
           SELECT RequestId, DATE(MAX(`Arrival Date`)) AS LastDate
             FROM Travelers
            GROUP BY RequestId) AS t
      ON t.RequestId = r.RequestId
   WHERE Status IN ('Approved', 'Denied', 'Other Resolution', 'Admin Close')
     AND (LastDate IS NULL
          OR DATEDIFF(LastDate, DATE(r.CreatedAt)) < -10
          OR DATEDIFF(LastDate, DATE(r.CreatedAt)) > 180)
   GROUP BY DATE(r.UpdatedAt)
   ORDER BY DATE(r.UpdatedAt);

  INSERT INTO ArchiveDateSummary (ArchiveDate, DeleteDate, RequestCount)
  SELECT ArchiveDate, DeleteDate, SUM(RequestCount)
    FROM ArchiveDateCount
   GROUP BY ArchiveDate, DeleteDate;

END$$

DROP VIEW IF EXISTS ArchiveStatus;

CREATE VIEW ArchiveStatus
    AS
    SELECT r.Status AS RequestStatus, f.Status AS FileStatus,
              Archived,
              COUNT(DISTINCT(o.RequestId)) AS RequestCount,
              COUNT(f.ArchiveFileId) AS FileCount
         FROM Requests o
         LEFT JOIN ArchivedRequests r
           ON r.RequestId = o.RequestId
         LEFT JOIN ArchivedFiles f
           ON f.RequestId = o.RequestId
        WHERE o.Status IN ('Approved', 'Denied', 'Other Resolution', 'Admin Close')
        GROUP BY RequestStatus, FileStatus, Archived
        ORDER BY RequestStatus, FileStatus, Archived
;
$$

DELIMITER ;
