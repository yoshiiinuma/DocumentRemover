
CREATE TABLE IF NOT EXISTS Users
(
  UserId VARCHAR(10) NOT NULL,
  `First Name` VARCHAR(255),
  `Last Name` VARCHAR(255),
  Email VARCHAR(255),
  Company VARCHAR(255),
  PRIMARY KEY (UserId)
);

CREATE TABLE IF NOT EXISTS Requests
(
  RequestId VARCHAR(10) NOT NULL,
  UserId VARCHAR(10),
  Owner VARCHAR(255),
  `Application Confirmation ID` VARCHAR(255),
  `Request Date` DATETIME DEFAULT CURRENT_TIMESTAMP,
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
  LetterFromMedicalProviderDesc TEXT,
  `Nucleic Acid Amplification Test` TEXT,
  `Nucleic Acid Amplification Test Reviewed?` TINYINT,
  NucleicAcidAmplificationTestDesc TEXT,
  `Requestor` VARCHAR(255),
  `Requestor Name` VARCHAR(255),
  `Requestor Email` VARCHAR(255),
  `Generating Base Email?` TINYINT,
  `Sending Received?` TINYINT,
  `Sending Updates?` TINYINT,
  `Sending Processing?` TINYINT,
  Archived TINYINT DEFAULT 0,
  ForceUpdate TINYINT DEFAULT 0,
  CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
  UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UpdatedBy VARCHAR(255),
  PRIMARY KEY (RequestId)
);

CREATE INDEX Request_User_IX on Requests(UserId, RequestId, `Request Date`);

CREATE INDEX Request_ReqDate_IX on Requests(`Request Date`, RequestId);

CREATE INDEX Request_Status_IX on Requests(Status, `Request Date`, RequestId);

CREATE INDEX Request_AppId_IX on Requests(`Application Confirmation ID`, RequestId);

CREATE INDEX Request_ApprovalId_IX on Requests(`Approval ID`, RequestId);


CREATE TABLE IF NOT EXISTS Travelers
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
  CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
  UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UpdatedBy VARCHAR(255),
  PRIMARY KEY (TravelerId)
);

CREATE INDEX Traveler_IX on Travelers(RequestId, TravelerId, Owner);


CREATE TABLE IF NOT EXISTS Documents
(
  RequestId VARCHAR(10),
  DocumentId VARCHAR(10) NOT NULL,
  Owner VARCHAR(255),
  Type VARCHAR(255),
  `Reviewed?` TINYINT,
  File TEXT,
  CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
  UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UpdatedBy VARCHAR(255),
  PRIMARY KEY (DocumentId)
);

CREATE INDEX Document_IX on Documents(RequestId, DocumentId, Owner);

CREATE TABLE IF NOT EXISTS Notes
(
  RequestId VARCHAR(10),
  NoteId VARCHAR(10) NOT NULL,
  Note MEDIUMTEXT,
  CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
  CreatedBy VARCHAR(255),
  UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UpdatedBy VARCHAR(255),
  PRIMARY KEY (NoteId)
);

CREATE INDEX Note_IX on Notes(RequestId, NoteId);


CREATE TABLE IF NOT EXISTS Communications
(
  RequestId VARCHAR(10),
  CommunicationId VARCHAR(10) NOT NULL,
  Status VARCHAR(64),
  Type VARCHAR(64),
  `To Address` VARCHAR(255),
  Subject VARCHAR(255),
  Content MEDIUMTEXT,
  CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
  CreatedBy VARCHAR(255),
  UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UpdatedBy VARCHAR(255),
  Requestor VARCHAR(255),
  PRIMARY KEY (CommunicationId)
);

CREATE INDEX Communication_IX on Communications(RequestId, CommunicationId);


CREATE TABLE IF NOT EXISTS Tags
(
  TagId VARCHAR(10) NOT NULL,
  Owner VARCHAR(255),
  Private TINYINT,
  Name VARCHAR(255),
  PRIMARY KEY (TagId)
);

CREATE INDEX Tag_IX on Tags(Owner, TagId, Name);


CREATE TABLE IF NOT EXISTS Filters
(
  FilterId VARCHAR(10) NOT NULL,
  TagId VARCHAR(10),
  RequestId VARCHAR(10),
  Owner VARCHAR(255),
  PRIMARY KEY (FilterId)
);

CREATE INDEX Filter_IX on Filters(TagId, RequestId);


CREATE TABLE IF NOT EXISTS States
(
  Value VARCHAR(64) NOT NULL,
  PRIMARY KEY (Value)
);

INSERT INTO States (Value)
VALUES
  ('Alabama'),
  ('Alaska'),
  ('Arizona'),
  ('Arkansas'),
  ('California'),
  ('Colorado'),
  ('Connecticut'),
  ('Delaware'),
  ('Florida'),
  ('Georgia'),
  ('Hawaii'),
  ('Idaho'),
  ('Illinois'),
  ('Indiana'),
  ('Iowa'),
  ('Kansas'),
  ('Kentucky'),
  ('Louisiana'),
  ('Maine'),
  ('Maryland'),
  ('Massachusetts'),
  ('Michigan'),
  ('Minnesota'),
  ('Mississippi'),
  ('Missouri'),
  ('Montana'),
  ('Nebraska'),
  ('Nevada'),
  ('New Hampshire'),
  ('New Jersey'),
  ('New Mexico'),
  ('New York'),
  ('North Carolina'),
  ('North Dakota'),
  ('Ohio'),
  ('Oklahoma'),
  ('Oregon'),
  ('Pennsylvania'),
  ('Rhode Island'),
  ('South Carolina'),
  ('South Dakota'),
  ('Tennessee'),
  ('Texas'),
  ('Utah'),
  ('Vermont'),
  ('Virginia'),
  ('Washington'),
  ('West Virginia'),
  ('Wisconsin'),
  ('Wyoming')

