
CREATE TABLE IF NOT EXISTS Organizations
(
  OrganizationId VARCHAR(10) NOT NULL,
  `Organization Name` VARCHAR(255),
  Address VARCHAR(512),
  Phone VARCHAR(128),
  Email VARCHAR(255),
  `Contact Email` VARCHAR(255),
  `Contact Name` VARCHAR(255),
  `Contact Title` VARCHAR(255),
  Status VARCHAR(64),
  SendingEmail TINYINT DEFAULT 0,
  Owner VARCHAR(255),
  CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
  CreatedBy VARCHAR(255),
  UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UpdatedBy VARCHAR(255),
  PRIMARY KEY (OrganizationId)
);

CREATE INDEX Organization_Email_IX on Organizations(Email);
CREATE INDEX Organization_ContactEmail_IX on Organizations(`Contact Email`);
CREATE INDEX Organization_Name_IX on Organizations(`Contact Name`);
CREATE INDEX Organization_ContactName_IX on Organizations(`Contact Name`);


CREATE TABLE IF NOT EXISTS Members
(
  OrganizationId VARCHAR(10),
  MemberId VARCHAR(10) NOT NULL,
  `Approval ID` VARCHAR(10),
  Status VARCHAR(10) DEFAULT 'Inactive',
  `First Name` VARCHAR(255),
  `Middle Name` VARCHAR(255),
  `Last Name` VARCHAR(255),
  Email VARCHAR(255),
  SendingEmail TINYINT DEFAULT 0,
  Owner VARCHAR(255),
  CreatedBy VARCHAR(255),
  UpdatedBy VARCHAR(255),
  CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
  UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (MemberId)
);

CREATE INDEX Member_IX on Members(OrganizationId, MemberId);
CREATE INDEX Member_Approval_IX on Members(`Approval Id`);


CREATE TABLE IF NOT EXISTS Affidavits
(
  AffidavitId VARCHAR(10) NOT NULL,
  OrganizationId VARCHAR(10),
  PageHeader TEXT,
  RepresentativeHeader TEXT,
  `Representative Name` VARCHAR(255),
  `Representative Title` VARCHAR(255),
  OrganizationHeader TEXT,
  `Organization Name` VARCHAR(255),
  Address VARCHAR(512),
  Phone VARCHAR(128),
  Email VARCHAR(255),
  ContentHeader TEXT,
  `Commission Expiration Date` DATE,
  `Agreed?` VARCHAR(3),
  Signature TEXT,
  SignedDate DATE,
  Owner VARCHAR(255),
  CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
  CreatedBy VARCHAR(255),
  PRIMARY KEY (AffidavitId)
);

CREATE INDEX Affidavit_OrgId_IX on Affidavits(OrganizationId);
CREATE INDEX Affidavit_OrgName_IX on Affidavits(`Organization Name`);

