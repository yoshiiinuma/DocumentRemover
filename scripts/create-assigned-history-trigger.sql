
DELIMITER $$

CREATE TRIGGER AssignedHistoryTrigger
  BEFORE UPDATE ON Requests
  FOR EACH ROW
BEGIN
  IF (NEW.Assigned IS NOT NULL AND NEW.Assigned <> '') THEN
    IF (OLD.Assigned IS NULL OR OLD.Assigned = '') THEN
      SET NEW.AssignedHistory = NEW.Assigned;
    ELSE
      IF (NEW.Assigned <> OLD.Assigned) THEN
        SET NEW.AssignedHistory = CONCAT(NEW.Assigned, ' < ', OLD.AssignedHistory);
      END IF;
    END IF;
  END IF;
END$$

DELIMITER ;
