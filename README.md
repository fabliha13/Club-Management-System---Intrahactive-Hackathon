# OCA IntraHacktive Club Management System

## Project Overview

The OCA IntraHacktive Club Management System is a Django-based web application designed for managing events, room bookings, budgets, and communications between the Office of Co-curricular Activities (OCA) and club panel members. The system provides secure, role-based dashboards with functionalities to streamline club management and approval processes.

### Key Features

1. **Role-Based Access**: 
   - **OCA (Office of Co-curricular Activities)** and **Club Panel Members** have distinct dashboards and permissions.
   
2. **Event Management**:
   - Club members can create and submit events for approval. 
   - OCA can approve, reject, or view events, with timestamps and approval notes recorded in the system.

3. **Room Booking**:
   - Club members can book predefined rooms, specifying the event, purpose, date, and time.
   - Available rooms include attributes like room name, location, and capacity, displayed in the room selection form.

4. **Budget Management**:
   - Club members can submit budget requests for events.
   - OCA can review and approve budgets, with approval or rejection status updates and detailed budget descriptions.

5. **Real-Time Messaging**:
   - Two-way communication system allowing messages between OCA and club members.
   - Messages are timestamped, with sender and receiver details stored in the backend.

6. **Event Reporting**:
   - Club members can generate reports for events, including attendance, total budget used, and room booking details.

### Backend Structure and Relationships

- **Models**:
  - **`club_panel`**: Links `User` profiles with specific clubs and tracks their membership.
  - **`Event`**: Stores information about events, linking to `club_panel` and storing approval details.
  - **`Room`**: Predefined rooms with properties like name, location, and capacity, used for room bookings.
  - **`RoomBooking`**: Relates events to rooms, recording booking dates and times.
  - **`BudgetRequest`**: Manages budget requests for events, linking to specific events and storing approval status.
  - **`Communication`**: Supports real-time messaging between users, with sender and receiver tracking.
  - **`EventReport`**: Aggregates event details into reports, linking to `RoomBooking` for room usage in events.

### How to Run Locally

1. Clone the repository.
2. Create a virtual environment and install dependencies.
3. Run database migrations.
4. Start the Django development server.

### Future Enhancements

Planned features include:
- **Push Notifications** for real-time updates on request statuses.
- **Detailed Analytics Dashboard** for insights on club activities and budgets.

---

### License

This project is licensed under the MIT License.
