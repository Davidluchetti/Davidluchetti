--DROP TABLE IICS_EDW_LOAD_SETUP_CTL CASCADE;

CREATE TABLE IICS_EDW_LOAD_SETUP_CTL
(
   CTL_LOAD_ID          BIGINT                          not null,
   ETL_PROC_WID         VARCHAR2(256),
   INTEGRATION_ID       VARCHAR2(256),
   LOAD_DT              VARCHAR2(256),
   START_TS             TIMESTAMP,
   END_TS               TIMESTAMP,
   LOAD_STATUS          VARCHAR2(1 BYTE)                not null,
   LAST_UPDATE_DATE     TIMESTAMP
   );


ALTER TABLE IICS_EDW_LOAD_SETUP_CTL ADD UNIQUE (CTL_LOAD_ID);

ALTER TABLE IICS_EDW_LOAD_SETUP_CTL ADD  PRIMARY KEY (CTL_LOAD_ID);

----------------------------------------------------------------------------------------------------

--DROP TABLE IICS_EDW_LOAD_TASKFLOW_CTL CASCADE;

CREATE TABLE IICS_EDW_LOAD_TASKFLOW_CTL
(
TASKFLOW_LOAD_ID     BIGINT                          not null,
   CTL_LOAD_ID          BIGINT                          not null,
   ETL_PROC_WID         VARCHAR2(256),
   INTEGRATION_ID       VARCHAR2(256),
   PROJECT_NAME         VARCHAR2(256),
   FOLDER_NAME          VARCHAR2(256),
   TASKFLOW_NAME        VARCHAR2(256)                   not null,
   LOAD_DT              VARCHAR2(256),
   START_TS             TIMESTAMP,
   END_TS               TIMESTAMP,
   LOAD_STATUS          VARCHAR2(1 BYTE)                not null,
   LAST_UPDATE_DATE     TIMESTAMP
   );

ALTER TABLE IICS_EDW_LOAD_TASKFLOW_CTL ADD UNIQUE (TASKFLOW_LOAD_ID, CTL_LOAD_ID);

ALTER TABLE IICS_EDW_LOAD_TASKFLOW_CTL ADD  PRIMARY KEY (TASKFLOW_LOAD_ID, CTL_LOAD_ID);

ALTER TABLE IICS_EDW_LOAD_TASKFLOW_CTL ADD  FOREIGN KEY (CTL_LOAD_ID)
REFERENCES IICS_EDW_LOAD_SETUP_CTL (CTL_LOAD_ID);
    


   
--------------------------------------------------------------------------------------------------
   

--DROP TABLE IICS_EDW_LOAD_DETAILS_CTL CASCADE;

CREATE TABLE IICS_EDW_LOAD_DETAILS_CTL
(
   MTT_LOAD_ID          BIGINT                          not null,
   TASKFLOW_LOAD_ID     BIGINT                          not null,
   CTL_LOAD_ID          BIGINT                          not null,
   ETL_PROC_WID         VARCHAR2(256),
   INTEGRATION_ID       VARCHAR2(256),
   PROJECT_NAME         VARCHAR2(256),
   FOLDER_NAME          VARCHAR2(256),
   TASKFLOW_NAME        VARCHAR2(256)                   not null,
   MTT_NAME             VARCHAR2(256)                   not null,
   LOAD_DT              VARCHAR2(256),
   START_TS             TIMESTAMP,
   END_TS               TIMESTAMP,
   TOTAL_SUCCESS_READ_ROWS BIGINT                          not null,
   TOTAL_FAILED_READ_ROWS BIGINT                          not null,
   TOTAL_SUCCESS_TARGET_ROWS BIGINT                          not null,
   TOTAL_FAILED_TARGET_ROWS BIGINT                          not null,
   LOAD_STATUS          VARCHAR2(1 BYTE)                not null,
   LAST_UPDATE_DATE     TIMESTAMP
     );

ALTER TABLE IICS_EDW_LOAD_DETAILS_CTL ADD UNIQUE (MTT_LOAD_ID,TASKFLOW_LOAD_ID, CTL_LOAD_ID);

ALTER TABLE IICS_EDW_LOAD_DETAILS_CTL ADD PRIMARY KEY (MTT_LOAD_ID,TASKFLOW_LOAD_ID, CTL_LOAD_ID);

ALTER TABLE IICS_EDW_LOAD_DETAILS_CTL ADD FOREIGN KEY (TASKFLOW_LOAD_ID, CTL_LOAD_ID)
REFERENCES IICS_EDW_LOAD_TASKFLOW_CTL (TASKFLOW_LOAD_ID, CTL_LOAD_ID);

