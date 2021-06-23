
CREATE TABLE IF NOT EXISTS RequestLog
(
  RequestId VARCHAR(10),
  UserId VARCHAR(10),
  Owner VARCHAR(255),
  `Application Confirmation ID` VARCHAR(255),
  `Request Date` DATETIME,
  `Approval Date` DATETIME,
  Status VARCHAR(64),
  `Approval ID` VARCHAR(255),
  `Arrival Date` DATE,
  Assigned VARCHAR(64),
  `Assignee Group` VARCHAR(64),
  Assignees VARCHAR(512),
  Immediate VARCHAR(10),
  AssignedHistory VARCHAR(255),
  `Travel Type` VARCHAR(64),
  `Exemption Category` VARCHAR(128),
  Purpose VARCHAR(128),
  `CISA Sub Category` VARCHAR(128),
  `Details` MEDIUMTEXT,
  `Project Document 1` TEXT,
  `Project Document 1 Reviewed?` TINYINT,
  `Project Document 2` TEXT,
  `Project Document 2 Reviewed?` TINYINT,
  `Proof of Port of Embarkation` TEXT,
  `Proof of Port of Embarkation Reviewed?` TINYINT,
  `PCS Orders` TEXT,
  `PCS Orders Reviewed?` TINYINT,
  `Letter From Medical Provider` TEXT,
  `Letter From Medical Provider Reviewed?` TINYINT,
  `Nucleic Acid Amplification Test` TEXT,
  `Nucleic Acid Amplification Test Reviewed?` TINYINT,
  `Requestor` VARCHAR(255),
  `Requestor Name` VARCHAR(255),
  `Requestor Email` VARCHAR(255),
  `Generating Base Email?` TINYINT,
  `Sending Received?` TINYINT,
  `Sending Updates?` TINYINT,
  `Sending Processing?` TINYINT,
  CreatedAt DATETIME,
  UpdatedAt DATETIME,
  UpdatedBy VARCHAR(255),
  LoggedAt DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX RequestLog_IX on RequestLog(RequestId, LoggedAt);


CREATE TABLE IF NOT EXISTS TravelerLog
(
  RequestId VARCHAR(10),
  TravelerId VARCHAR(10) NOT NULL,
  Owner VARCHAR(255),
  `First Name` VARCHAR(255),
  `Middle Name` VARCHAR(255),
  `Last Name` VARCHAR(255),
  `Exemption Category` VARCHAR(128),
  `Origin Country` VARCHAR(128),
  `Origin State` VARCHAR(128),
  `Destination Island` VARCHAR(128),
  `Arrival Date` DATETIME,
  `Arrival Flight Number` VARCHAR(128),
  `Departure Date` DATETIME,
  `Departure Flight Number` VARCHAR(128),
  `Phone` VARCHAR(128),
  `Quarantine Location Type` VARCHAR(255),
  `Quarantine Location Address` TEXT,
  `Travel 14Days Before Arrival` TINYINT,
  `Recent Travels` TEXT,
  `Picture ID` TEXT,
  CreatedAt DATETIME,
  UpdatedAt DATETIME,
  UpdatedBy VARCHAR(255),
  LoggedAt DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX TravelerLog_IX on TravelerLog(RequestId, LoggedAt);
CREATE INDEX TravelerLog_Traveler_IX on TravelerLog(RequestId, TravelerId, LoggedAt);


