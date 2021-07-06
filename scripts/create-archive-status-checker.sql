DELIMITER $$

DROP PROCEDURE IF EXISTS CreateArchiveDates;

CREATE PROCEDURE CreateArchiveDates(IN days1 INT, IN days2 INT, IN days3 INT)
BEGIN
  SET days1 = IFNULL(days1 + 1, 61);
  SET days2 = IFNULL(days2 + 1, 241);
  SET days3 = IFNULL(days3, 30);

  DROP TEMPORARY TABLE IF EXISTS ArchiveDates;
  CREATE TEMPORARY TABLE ArchiveDates
  (
    RequestId VARCHAR(10),
    TargetDate DATE,
    ExpectedArchiveDate DATE,
    ExpectedDeleteDate DATE,
    ActualArchiveDate DATE,
    ActualDeleteDate DATE,
    Archived TINYINT
  );

  INSERT INTO ArchiveDates (RequestId, Archived, TargetDate,
                  ExpectedArchiveDate, ExpectedDeleteDate,
                  ActualArchiveDate, ActualDeleteDate)
  SELECT r.RequestId, Archived, LastDate,
         LastDate + INTERVAL days1 DAY,
         LastDate + INTERVAL days1 + days3 DAY,
         a.ArchiveDate, a.DeleteDate
    FROM Requests r
    LEFT JOIN (
           SELECT RequestId, DATE(MAX(`Arrival Date`)) AS LastDate
             FROM Travelers
            GROUP BY RequestId) AS t
      ON t.RequestId = r.RequestId
    LEFT JOIN ArchivedRequests a
      ON a.RequestId = r.RequestId
   WHERE r.Status IN ('Approved', 'Denied', 'Other Resolution', 'Admin Close')
     AND LastDate IS NOT NULL
     AND DATEDIFF(LastDate, DATE(r.CreatedAt)) >= -10
     AND DATEDIFF(LastDate, DATE(r.CreatedAt)) <= 180
   ORDER BY LastDate;

  INSERT INTO ArchiveDates (RequestId, Archived, TargetDate,
                  ExpectedArchiveDate, ExpectedDeleteDate,
                  ActualArchiveDate, ActualDeleteDate)
  SELECT r.RequestId, Archived, DATE(r.UpdatedAt),
         DATE(r.UpdatedAT) + INTERVAL days2 DAY,
         DATE(r.UpdatedAT) + INTERVAL days2 + days3 DAY,
         a.ArchiveDate, a.DeleteDate
    FROM Requests r
    LEFT JOIN (
           SELECT RequestId, DATE(MAX(`Arrival Date`)) AS LastDate
             FROM Travelers
            GROUP BY RequestId) AS t
      ON t.RequestId = r.RequestId
    LEFT JOIN ArchivedRequests a
      ON a.RequestId = r.RequestId
   WHERE r.Status IN ('Approved', 'Denied', 'Other Resolution', 'Admin Close')
     AND (LastDate IS NULL
          OR DATEDIFF(LastDate, DATE(r.CreatedAt)) < -10
          OR DATEDIFF(LastDate, DATE(r.CreatedAt)) > 180)
   ORDER BY DATE(r.UpdatedAt);

END$$

DELIMITER ;
