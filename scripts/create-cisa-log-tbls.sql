
CREATE TABLE IF NOT EXISTS OrganizationLog
(
  OrganizationId VARCHAR(10),
  OrganizationName VARCHAR(255),
  Address VARCHAR(512),
  Phone VARCHAR(128),
  Email VARCHAR(255),
  ContactEmail VARCHAR(255),
  ContactName VARCHAR(255),
  ContactTitle VARCHAR(255),
  Status VARCHAR(64),
  Owner VARCHAR(255),
  CreatedAt DATETIME,
  CreatedBy VARCHAR(255),
  UpdatedAt DATETIME,
  UpdatedBy VARCHAR(255),
  LoggedAt DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX Organization_Log_IX on OrganizationLog(OrganizationId, LoggedAt);

CREATE TABLE IF NOT EXISTS MemberLog
(
  OrganizationId VARCHAR(10),
  MemberId VARCHAR(10),
  ApprovalId VARCHAR(10),
  Status VARCHAR(10),
  FirstName VARCHAR(255),
  MiddleName VARCHAR(255),
  LastName VARCHAR(255),
  Email VARCHAR(255),
  Owner VARCHAR(255),
  CreatedBy VARCHAR(255),
  UpdatedBy VARCHAR(255),
  CreatedAt DATETIME,
  UpdatedAt DATETIME,
  LoggedAt DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX Member_Log_IX on MemberLog(OrganizationId, MemberId, LoggedAt);

CREATE TABLE IF NOT EXISTS AffidavitLog
(
  AffidavitId VARCHAR(10),
  OrganizationId VARCHAR(10),
  RepresentativeName VARCHAR(255),
  RepresentativeTitle VARCHAR(255),
  OrganizationName VARCHAR(255),
  Address VARCHAR(512),
  Phone VARCHAR(128),
  Email VARCHAR(255),
  CommissionExpirationDate DATE,
  Agreed VARCHAR(3),
  Signature TEXT,
  SignedDate DATE,
  Owner VARCHAR(255),
  CreatedAt DATETIME,
  CreatedBy VARCHAR(255),
  LoggedAt DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX Affidavit_Log_IX on AffidavitLog(AffidavitId, LoggedAt);

