
CREATE TABLE IF NOT EXISTS ArchivedRequests
(
  RequestId VARCHAR(10) PRIMARY KEY,
  Status TINYINT DEFAULT 0,
  ArchiveFolder VARCHAR(64),
  ArchiveDate DATE,
  DeleteDate DATE,
  CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
  UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE INDEX ArchivedRequests_Status_IX on ArchivedRequests(Status, RequestId);
CREATE INDEX ArchivedRequests_ArchiveDate_IX on ArchivedRequests(Status, ArchiveDate, RequestId);

CREATE TABLE IF NOT EXISTS ArchivedFiles
(
  ArchiveFileId INT AUTO_INCREMENT PRIMARY KEY,
  RequestId VARCHAR(10) NOT NULL,
  Status TINYINT DEFAULT 0,
  SrcFolder VARCHAR(64),
  FileId VARCHAR(64),
  OriginalId VARCHAR(10),
  OriginalType TINYINT,
  OriginalPath VARCHAR(255),
  OriginalFileName VARCHAR(255),
  FileExtension VARCHAR(64),
  MoveDate DATE,
  CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
  UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


CREATE INDEX ArchivedFiles_RequestId_IX on ArchivedFiles(RequestId, Status);
CREATE INDEX ArchivedFiles_FileId_IX on ArchivedFiles(FileId);


