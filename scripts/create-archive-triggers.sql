
DELIMITER $$

CREATE PROCEDURE CreateArchiveRequests(IN numOfDays INT)
BEGIN
  SET numOfDays = IFNULL(numOfDays, 60);

  INSERT INTO ArchivedRequests(RequestId)
  SELECT r.RequestId
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
     AND LastDate < DATE_SUB(CURRENT_DATE, INTERVAL numOfDays DAY);
END$$

CREATE PROCEDURE CreateArchiveRequestsWithInvalidDate(IN numOfDays INT)
BEGIN
  SET numOfDays = IFNULL(numOfDays, 240);

  INSERT INTO ArchivedRequests(RequestId)
  SELECT r.RequestId
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
     AND DATE(UpdatedAt) < DATE_SUB(CURRENT_DATE, INTERVAL numOfDays DAY);
END$$

CREATE PROCEDURE InsertArchiveFile(IN reqId VARCHAR(10), IN originalId VARCHAR(10), IN fileName TEXT, IN fileType TINYINT)
BEGIN
  IF (reqId IS NOT NULL AND originalId IS NOT NULL AND fileName IS NOT NULL AND LENGTH(fileName) > 0) THEN
    INSERT
      INTO ArchivedFiles(RequestId, OriginalId, OriginalPath, OriginalType)
    VALUES (reqId, originalId, fileName, fileType);
  END IF;
END$$

CREATE PROCEDURE InsertArchiveFiles(IN reqId VARCHAR(10))
BEGIN
  DECLARE fname1 TEXT;
  DECLARE fname2 TEXT;
  DECLARE fname3 TEXT;
  DECLARE fname4 TEXT;
  DECLARE fname5 TEXT;
  DECLARE fname6 TEXT;

  SELECT `Project Document 1`,
         `Project Document 2`,
         `Proof of Port of Embarkation`,
         `PCS Orders`,
         `Letter From Medical Provider`,
         `Nucleic Acid Amplification Test`
    INTO fname1, fname2, fname3, fname4, fname5, fname6
    FROM Requests r
   WHERE RequestId = reqId;

  CALL InsertArchiveFile(reqId, reqId, fname1, 1);
  CALL InsertArchiveFile(reqId, reqId, fname2, 2);
  CALL InsertArchiveFile(reqId, reqId, fname3, 3);
  CALL InsertArchiveFile(reqId, reqId, fname4, 4);
  CALL InsertArchiveFile(reqId, reqId, fname5, 5);
  CALL InsertArchiveFile(reqId, reqId, fname6, 6);

  INSERT INTO ArchivedFiles(RequestId, OriginalId, OriginalPath, OriginalType)
  SELECT RequestId, TravelerId, `Picture ID`, 7
    FROM Travelers
   WHERE RequestId = reqId
     AND LENGTH(`Picture ID`) > 0;

  INSERT INTO ArchivedFiles(RequestId, OriginalId, OriginalPath, OriginalType)
  SELECT RequestId, DocumentId, File, 8
    FROM Documents
   WHERE RequestId = reqId
     AND LENGTH(File) > 0;
END$$

CREATE PROCEDURE CreateArchiveFiles()
BEGIN
  DECLARE reqId VARCHAR(10);
  DECLARE done BOOLEAN DEFAULT FALSE;

  DECLARE requestCursor
   CURSOR FOR
   SELECT RequestId
     FROM ArchivedRequests
    WHERE Status = 0;

  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

  START TRANSACTION;

  OPEN requestCursor;

  fetchLoop: LOOP
    FETCH requestCursor INTO reqId;
    IF done THEN
      LEAVE fetchLoop;
    END IF;
    call InsertArchiveFiles(reqId);
  END LOOP fetchLoop;

  CLOSE requestCursor;

  UPDATE ArchivedRequests
     SET Status = 1
   WHERE Status = 0;

   COMMIT;
END$$

CREATE PROCEDURE SetDeletedFileImage()
BEGIN
  START TRANSACTION;

  UPDATE Travelers t
    JOIN ArchivedRequests a
      ON a.RequestId = t.RequestId
     SET `Picture ID` = 'FileDeleted.png',
         t.UpdatedBy = 'SYSTEMUSER'
   WHERE a.Status = 2;

  UPDATE Documents d
    JOIN ArchivedRequests a
      ON a.RequestId = d.RequestId
     SET File = 'FileDeleted.png',
         d.UpdatedBy = 'SYSTEMUSER'
   WHERE a.Status = 2;

  UPDATE Requests r
    JOIN ArchivedRequests a
      ON a.RequestId = r.RequestId
     SET `Project Document 1` = IF(`Project Document 1` IS NULL OR `Project Document 1` = '', NULL, 'FileDeleted.png'),
         `Project Document 2` = IF(`Project Document 2` IS NULL OR `Project Document 2` = '', NULL, 'FileDeleted.png'),
         `Proof of Port of Embarkation` = IF(`Proof of Port of Embarkation` IS NULL OR `Proof of Port of Embarkation` = '', NULL, 'FileDeleted.png'),
         `PCS Orders` = IF(`PCS Orders` IS NULL OR `PCS Orders` = '', NULL, 'FileDeleted.png'),
         `Letter From Medical Provider` = IF(`Letter From Medical Provider` IS NULL OR `Letter From Medical Provider` = '', NULL, 'FileDeleted.png'),
         `Nucleic Acid Amplification Test` = IF(`Nucleic Acid Amplification Test` IS NULL OR `Nucleic Acid Amplification Test` = '', NULL, 'FileDeleted.png'),
         r.UpdatedBy = 'SYSTEMUSER'
   WHERE a.Status = 2;

  UPDATE ArchivedRequests
     SET Status = 3
   WHERE Status = 2;

  COMMIT;
END$$

CREATE PROCEDURE SetArchiveFlagToRequests()
BEGIN
  UPDATE Requests r
    JOIN ArchivedRequests a
      ON a.RequestId = r.RequestId
     SET r.Archived = 1,
         r.UpdatedBy = 'SYSTEMUSER',
         a.Status = 4
   WHERE a.Status = 3; 
END$$

CREATE PROCEDURE CreateUploadFiles()
BEGIN

  DROP TEMPORARY TABLE IF EXISTS UploadedFiles;

  CREATE TEMPORARY TABLE UploadedFiles
  (
    RequestId VARCHAR(10) NOT NULL,
    OriginId VARCHAR(10) NOT NULL,
    FileType TINYINT,
    FilePath TEXT
  );

  INSERT INTO UploadedFiles (RequestId, OriginId, FileType, FilePath)
  SELECT RequestId, RequestId, 1, `Project Document 1`
    FROM Requests
   WHERE LENGTH(`Project Document 1`) > 0;

  INSERT INTO UploadedFiles (RequestId, OriginId, FileType, FilePath)
  SELECT RequestId, RequestId, 2, `Project Document 2`
    FROM Requests
   WHERE LENGTH(`Project Document 2`) > 0;

  INSERT INTO UploadedFiles (RequestId, OriginId, FileType, FilePath)
  SELECT RequestId, RequestId, 3, `Proof of Port of Embarkation`
    FROM Requests
   WHERE LENGTH(`Proof of Port of Embarkation`) > 0;

  INSERT INTO UploadedFiles (RequestId, OriginId, FileType, FilePath)
  SELECT RequestId, RequestId, 4, `PCS Orders`
    FROM Requests
   WHERE LENGTH(`PCS Orders`) > 0;

  INSERT INTO UploadedFiles (RequestId, OriginId, FileType, FilePath)
  SELECT RequestId, RequestId, 5, `Letter From Medical Provider`
    FROM Requests
   WHERE LENGTH(`Letter From Medical Provider`) > 0;

  INSERT INTO UploadedFiles (RequestId, OriginId, FileType, FilePath)
  SELECT RequestId, RequestId, 6, `Nucleic Acid Amplification Test`
    FROM Requests
   WHERE LENGTH(`Nucleic Acid Amplification Test`) > 0;

  INSERT INTO UploadedFiles (RequestId, OriginId, FileType, FilePath)
  SELECT RequestId, TravelerId, 7, `Picture ID`
    FROM Travelers
   WHERE LENGTH(`Picture ID`) > 0;

  INSERT INTO UploadedFiles (RequestId, OriginId, FileType, FilePath)
  SELECT RequestId, DocumentId, 8, File
    FROM Documents
   WHERE LENGTH(File) > 0;

END$$

DELIMITER ;


