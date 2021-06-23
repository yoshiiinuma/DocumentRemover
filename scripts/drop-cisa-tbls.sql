
DROP INDEX Affidavit_OrgId_IX on Affidavits;
DROP INDEX Affidavit_OrgName_IX on Affidavits;

DROP INDEX Member_IX on Members;
DROP INDEX Member_Approval_IX on Members;

DROP INDEX Organization_Email_IX on Organizations;
DROP INDEX Organization_ContactEmail_IX on Organizations;
DROP INDEX Organization_Name_IX on Organizations;
DROP INDEX Organization_ContactName_IX on Organizations;

DROP TABLE IF EXISTS Affidavits;
DROP TABLE IF EXISTS Members;
DROP TABLE IF EXISTS Organizations;
