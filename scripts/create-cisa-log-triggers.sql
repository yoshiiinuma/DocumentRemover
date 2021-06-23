
DELIMITER $$

CREATE TRIGGER OrganizationLogTrigger
  BEFORE UPDATE ON Organizations
  FOR EACH ROW
BEGIN
  INSERT INTO OrganizationLog (
    OrganizationId, OrganizationName, Address, Phone,
    Email, ContactEmail, ContactName,
    Status, Owner,
    CreatedAt, CreatedBy, UpdatedAt, UpdatedBy)
  VALUES (
    OLD.OrganizationId, OLD.`Organization Name`, OLD.Address, OLD.Phone,
    OLD.Email, OLD.`Contact Email`, OLD.`Contact Name`,
    OLD.Status, OLD.Owner,
    OLD.CreatedAt, OLD.CreatedBy, OLD.UpdatedAt, OLD.UpdatedBy);
END$$

CREATE TRIGGER MemberLogTrigger
  BEFORE UPDATE ON Members
  FOR EACH ROW
BEGIN
  INSERT INTO MemberLog (
    OrganizationId, MemberId, ApprovalId, Status,
    FirstName, MiddleName, LastName, Email, Owner,
    CreatedBy, UpdatedBy, CreatedAt, UpdatedAt)
  VALUES (
    OLD.OrganizationId, OLD.MemberId, OLD.`Approval ID`, OLD.Status,
    OLD.`First Name`, OLD.`Middle Name`, OLD.`Last Name`, OLD.Email, OLD.Owner,
    OLD.CreatedBy, OLD.UpdatedBy, OLD.CreatedAt, OLD.UpdatedAt);
END$$

CREATE TRIGGER AffidavitLogTrigger
  AFTER INSERT ON Affidavits
  FOR EACH ROW
BEGIN
  INSERT INTO AffidavitLog (
    AffidavitId, OrganizationId,
    RepresentativeName, RepresentativeTitle,
    OrganizationName, Address, Phone, Email,
    CommissionExpirationDate,
    Agreed, Signature, SignedDate, Owner,
    CreatedAt, CreatedBy)
  VALUES (
    NEW.AffidavitId, NEW.OrganizationId,
    NEW.`Representative Name`, NEW.`Representative Title`,
    NEW.`Organization Name`, NEW.Address, NEW.Phone, NEW.Email,
    NEW.`Commission Expiration Date`,
    NEW.`Agreed?`, NEW.Signature, NEW.SignedDate, NEW.Owner,
    NEW.CreatedAt, NEW.CreatedBy);
END$$

DELIMITER ;
