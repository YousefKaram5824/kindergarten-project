# TODO: Integrate FullDayProgramDTO and IndividualSessionDTO in add_child_ui

## Tasks
- [x] Import CreateFullDayProgramDTO, CreateIndividualSessionDTO, FullDayProgramService, IndividualSessionService in add_child_ui.py
- [x] Modify add_child function to create program/session DTO after creating child
- [x] For FULL_DAY child_type: create CreateFullDayProgramDTO with monthly_fee, bus_fee, entry_date, child_id
- [x] For SESSIONS child_type: create CreateIndividualSessionDTO with session_fee, monthly_sessions_count, entry_date, child_id
- [x] Call appropriate service to create the program/session record
- [x] Add all required fields to DTOs (diagnosis, tests_applied, etc.)
- [x] Add UI fields for additional program/session data (diagnosis, tests_applied, training_plan, etc.)
- [x] Update add_child function to collect UI values for additional fields
- [x] Update on_checkbox_change to show/hide additional fields based on child type
- [x] Update reset_form to reset all new fields
- [ ] Test adding children of both types to verify data is stored correctly
