-- ====================================================================
-- Project: FixTrack — Campus Repair and Maintenance Tracker
-- Target Schema: FIXTRACK
-- Service: FREEPDB1
-- Description: Complete backend objects (Data, Procedures, Functions, Trigger, View)
-- ====================================================================

-- --------------------------------------------------------------------
-- 1. Insert Sample Maintenance Requests (Avoids Duplicate Inserts)
-- --------------------------------------------------------------------
MERGE INTO REQUESTS r
USING (
    SELECT 'Classroom lights not working' AS TITLE, 'Lights flickering and two tubes completely off in Room 204' AS DESCRIPTION, 'Block A, Room 204' AS LOCATION, 1 AS CATEGORY_ID, 1 AS SUBMITTED_BY, NULL AS ASSIGNED_TO, 'HIGH' AS PRIORITY, 'PENDING' AS STATUS FROM DUAL UNION ALL
    SELECT 'Water leakage in washroom', 'Continuous tap leak leading to water logging', 'Block B, 2nd Floor Washroom', 2, 2, NULL, 'MEDIUM', 'IN PROGRESS' FROM DUAL UNION ALL
    SELECT 'Broken classroom chair', 'Two desk chairs have broken backrests', 'Block C, Room 102', 3, 3, NULL, 'HIGH', 'PENDING' FROM DUAL UNION ALL
    SELECT 'Wi-Fi connection unavailable', 'Signal drops frequently during lab hours', 'Computer Lab 3', 5, 1, 4, 'MEDIUM', 'IN PROGRESS' FROM DUAL UNION ALL
    SELECT 'Classroom cleaning required', 'Floor needs sweeping and dustbins emptied', 'Seminar Hall 1', 4, 2, 5, 'LOW', 'RESOLVED' FROM DUAL
) s
ON (r.TITLE = s.TITLE AND r.LOCATION = s.LOCATION)
WHEN NOT MATCHED THEN
INSERT (TITLE, DESCRIPTION, LOCATION, CATEGORY_ID, SUBMITTED_BY, ASSIGNED_TO, PRIORITY, STATUS, RESOLVED_AT)
VALUES (s.TITLE, s.DESCRIPTION, s.LOCATION, s.CATEGORY_ID, s.SUBMITTED_BY, s.ASSIGNED_TO, s.PRIORITY, s.STATUS, 
        CASE WHEN s.STATUS = 'RESOLVED' THEN SYSTIMESTAMP ELSE NULL END);

COMMIT;

-- --------------------------------------------------------------------
-- 2. Stored Procedures
-- --------------------------------------------------------------------

-- Procedure 1: SUBMIT_REQUEST
-- Purpose: Inserts a new request submitted by a student and returns the generated REQUEST_ID
CREATE OR REPLACE PROCEDURE SUBMIT_REQUEST (
    p_title        IN  REQUESTS.TITLE%TYPE,
    p_description  IN  REQUESTS.DESCRIPTION%TYPE,
    p_location     IN  REQUESTS.LOCATION%TYPE,
    p_category_id  IN  REQUESTS.CATEGORY_ID%TYPE,
    p_submitted_by IN  REQUESTS.SUBMITTED_BY%TYPE,
    p_priority     IN  REQUESTS.PRIORITY%TYPE,
    p_request_id   OUT REQUESTS.REQUEST_ID%TYPE
) AS
BEGIN
    INSERT INTO REQUESTS (
        TITLE, DESCRIPTION, LOCATION, CATEGORY_ID, SUBMITTED_BY, PRIORITY, STATUS, CREATED_AT, UPDATED_AT
    ) VALUES (
        p_title, p_description, p_location, p_category_id, p_submitted_by, p_priority, 'PENDING', SYSTIMESTAMP, SYSTIMESTAMP
    ) RETURNING REQUEST_ID INTO p_request_id;
END SUBMIT_REQUEST;
/

-- Procedure 2: ASSIGN_REQUEST
-- Purpose: Assigns a request to a staff member and updates request status
CREATE OR REPLACE PROCEDURE ASSIGN_REQUEST (
    p_request_id   IN REQUESTS.REQUEST_ID%TYPE,
    p_assigned_to  IN REQUESTS.ASSIGNED_TO%TYPE
) AS
    v_role VARCHAR2(20);
BEGIN
    SELECT USER_ROLE INTO v_role FROM USERS WHERE USER_ID = p_assigned_to;
    
    IF v_role != 'STAFF' THEN
        RAISE_APPLICATION_ERROR(-20001, 'Assignment failed: Selected user must have the STAFF role.');
    END IF;

    UPDATE REQUESTS
    SET ASSIGNED_TO = p_assigned_to,
        STATUS = CASE WHEN STATUS = 'PENDING' THEN 'IN PROGRESS' ELSE STATUS END,
        UPDATED_AT = SYSTIMESTAMP
    WHERE REQUEST_ID = p_request_id;
END ASSIGN_REQUEST;
/

-- Procedure 3: UPDATE_REQUEST_STATUS
-- Purpose: Updates status and sets RESOLVED_AT timestamp when resolved
CREATE OR REPLACE PROCEDURE UPDATE_REQUEST_STATUS (
    p_request_id  IN REQUESTS.REQUEST_ID%TYPE,
    p_new_status  IN REQUESTS.STATUS%TYPE
) AS
BEGIN
    UPDATE REQUESTS
    SET STATUS = p_new_status,
        RESOLVED_AT = CASE WHEN p_new_status = 'RESOLVED' THEN SYSTIMESTAMP ELSE NULL END,
        UPDATED_AT = SYSTIMESTAMP
    WHERE REQUEST_ID = p_request_id;
END UPDATE_REQUEST_STATUS;
/

-- --------------------------------------------------------------------
-- 3. Database Functions
-- --------------------------------------------------------------------

-- Function 1: GET_PENDING_COUNT
CREATE OR REPLACE FUNCTION GET_PENDING_COUNT RETURN NUMBER AS
    v_count NUMBER := 0;
BEGIN
    SELECT COUNT(*) INTO v_count FROM REQUESTS WHERE STATUS = 'PENDING';
    RETURN v_count;
END GET_PENDING_COUNT;
/

-- Function 2: GET_RESOLVED_COUNT
CREATE OR REPLACE FUNCTION GET_RESOLVED_COUNT RETURN NUMBER AS
    v_count NUMBER := 0;
BEGIN
    SELECT COUNT(*) INTO v_count FROM REQUESTS WHERE STATUS = 'RESOLVED';
    RETURN v_count;
END GET_RESOLVED_COUNT;
/

-- --------------------------------------------------------------------
-- 4. Database Trigger
-- --------------------------------------------------------------------

-- Trigger: TRG_UPDATE_REQUEST_TIMESTAMP
-- Purpose: Automatically updates UPDATED_AT whenever any column in REQUESTS is updated
CREATE OR REPLACE TRIGGER TRG_UPDATE_REQUEST_TIMESTAMP
BEFORE UPDATE ON REQUESTS
FOR EACH ROW
BEGIN
    :NEW.UPDATED_AT := SYSTIMESTAMP;
END;
/

-- --------------------------------------------------------------------
-- 5. Database View
-- --------------------------------------------------------------------

-- View: VIEW_ALL_REQUESTS
-- Purpose: Denormalized view with clean JOINs for frontend tables
CREATE OR REPLACE VIEW VIEW_ALL_REQUESTS AS
SELECT 
    r.REQUEST_ID,
    r.TITLE,
    r.DESCRIPTION,
    r.LOCATION,
    c.CATEGORY_NAME,
    c.CATEGORY_ID,
    u_sub.FULL_NAME AS SUBMITTED_BY_NAME,
    r.SUBMITTED_BY,
    NVL(u_asg.FULL_NAME, 'Unassigned') AS ASSIGNED_TO_NAME,
    r.ASSIGNED_TO,
    r.PRIORITY,
    r.STATUS,
    TO_CHAR(r.CREATED_AT, 'YYYY-MM-DD HH24:MI') AS CREATED_DATE,
    TO_CHAR(r.UPDATED_AT, 'YYYY-MM-DD HH24:MI') AS UPDATED_DATE,
    TO_CHAR(r.RESOLVED_AT, 'YYYY-MM-DD HH24:MI') AS RESOLVED_DATE
FROM REQUESTS r
JOIN CATEGORIES c ON r.CATEGORY_ID = c.CATEGORY_ID
JOIN USERS u_sub ON r.SUBMITTED_BY = u_sub.USER_ID
LEFT JOIN USERS u_asg ON r.ASSIGNED_TO = u_asg.USER_ID;

COMMIT;


SELECT OBJECT_TYPE, OBJECT_NAME, STATUS 
FROM USER_OBJECTS 
WHERE OBJECT_NAME IN (
    'REQUESTS', 'SUBMIT_REQUEST', 'ASSIGN_REQUEST', 
    'UPDATE_REQUEST_STATUS', 'GET_PENDING_COUNT', 
    'GET_RESOLVED_COUNT', 'TRG_UPDATE_REQUEST_TIMESTAMP', 
    'VIEW_ALL_REQUESTS'
)
ORDER BY OBJECT_TYPE, OBJECT_NAME;