DELIMITER $$

CREATE TRIGGER ValidateRequestStatus BEFORE UPDATE ON Requests
FOR EACH ROW
BEGIN
  DECLARE errMsg VARCHAR(255);
  SET errMsg = CONCAT('Invalid Status CURRENT: "', OLD.Status, '" > NEW: "', NEW.Status, '" Updated By ', NEW.UpdatedBy);
  
  IF NEW.ForceUpdate <> 1 THEN

    IF NEW.Status = 'Submitted' AND OLD.Status NOT IN ('Draft', 'Submitted') THEN
      SIGNAL SQLSTATE '45000'
         SET MESSAGE_TEXT = errMsg;
    END IF;
    IF NEW.Status = 'Reviewing' AND OLD.Status NOT IN('Submitted', 'Update Required', 'Reviewing') THEN
      SIGNAL SQLSTATE '45000'
         SET MESSAGE_TEXT = errMsg;
    END IF;
    IF NEW.Status = 'Update Required' AND OLD.Status NOT IN ('Reviewing', 'Update Required') THEN
      SIGNAL SQLSTATE '45000'
         SET MESSAGE_TEXT = errMsg;
    END IF;
    IF NEW.Status IN ('Approved', 'Denied', 'Other Resolution') AND OLD.Status NOT IN ('Reviewing') THEN
      SIGNAL SQLSTATE '45000'
         SET MESSAGE_TEXT = errMsg;
    END IF;
  
  END IF;

  SET NEW.ForceUpdate = 0; 
END$$   

DELIMITER ;
                                                                                            
