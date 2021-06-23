
DELIMITER $$

CREATE TRIGGER ArrivalDateUpdateTrigger
  AFTER UPDATE ON Travelers
  FOR EACH ROW
BEGIN
  DECLARE EarliestArrivalDate Date;
  SET @EarliestArrivalDate = (
        SELECT DATE(MIN(`Arrival Date`))
          FROM Travelers
         WHERE RequestId = NEW.RequestId
         GROUP BY RequestId);
  IF (@EarliestArrivalDate IS NOT NULL) THEN
    UPDATE Requests r
      SET r.`Arrival Date` = @EarliestArrivalDate,
          r.ForceUpdate = 1
      WHERE r.RequestId = NEW.RequestId;
  END IF;
END$$

CREATE TRIGGER ArrivalDateInsertTrigger
  AFTER INSERT ON Travelers
  FOR EACH ROW
BEGIN
  DECLARE EarliestArrivalDate Date;
  SET @EarliestArrivalDate = (
        SELECT DATE(MIN(`Arrival Date`))
          FROM Travelers
         WHERE RequestId = NEW.RequestId
         GROUP BY RequestId);
  IF (@EarliestArrivalDate IS NOT NULL) THEN
    UPDATE Requests r
      SET r.`Arrival Date` = @EarliestArrivalDate,
          r.ForceUpdate = 1
      WHERE r.RequestId = NEW.RequestId;
  END IF;
END$$

DELIMITER ;
