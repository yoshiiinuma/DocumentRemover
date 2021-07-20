
DELIMITER $$

CREATE EVENT RequestArchiveEvent
  ON SCHEDULE
      EVERY 1 DAY
      STARTS (TIMESTAMP(CURRENT_DATE) + INTERVAL 21 HOUR)
  ON COMPLETION PRESERVE
DO
BEGIN
  CALL CreateArchiveRequests(60, NULL);
  CALL CreateArchiveRequestsWithInvalidDate(240, NULL);
  CALL CreateArchiveFiles();
END$$

DELIMITER ;
