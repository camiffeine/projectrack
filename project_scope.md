# Part 2: Requirements Elicitation

## a) Initial Requirements Elicitation

In the initial meetings between group members during class time, discussions and brainstorming sessions were held regarding potential projects, given the course requirements and scope, as well as the available time. These meetings were supplemented with asynchronous communication.

Eventually, it was decided that the project would take an academic approach, focusing on higher education. This was based on the understanding that, as active university students, it would be easier to identify potential problems to solve, needs to meet, or even tools that could facilitate certain processes within the university environment. All of this was based on the general experiences of the development group.

Finally, the idea arose to centralize the tracking and virtual/asynchronous submission of projects, assignments, or tasks on a single platform. This was intended to address problems related to the lack of efficiency, coordination, and consistency between professors and students when assigning, submitting (partially or fully), and providing feedback on these academic projects.

It is known that, in the context of virtual or asynchronous submissions, more than one existing tool is often used for the aforementioned tasks. For example, email is used to assign submissions, Moodle or Classroom to obtain materials and submit them, and possibly email again for intermediate submissions or direct feedback. This virtual management model can lead to certain organizational difficulties, requiring constant switching between applications, potentially hindering the monitoring of submitted projects at each stage of development and facilitating feedback, leading to possible errors, delays, and a lack of transparency.

The aim is to provide a system where the target audience—teachers and students—finds practical and intuitive functionalities for creating specific groups or courses, assigning projects, submitting project progress or completed projects, and providing timely feedback; managing multiple projects; uploading project-related documents; and logging activities to track individual or group progress, among other features. The general expectation is that this system will simplify the interaction between teachers and students, minimizing the loss of information and improving the academic experience, all without losing features that provide quality of life to the growing need to digitize academic processes, such as the notifications of new assignments provided by platforms like Classroom.

As a team of engineering and software development students, we hope this project will allow us to put our programming, database, and project management skills into practice in a realistic context. As we acquire these skills, we will learn new tools, languages, and frameworks relevant to backend and frontend development, such as FastAPI and React, while also improving our collaborative teamwork and coordination skills, both in real time and asynchronously.

We also hope to contribute a potential solution adaptable to real-world educational settings as a potentially significant and tangible contribution to improving these academic processes.

## **b) Initial Requirement Identification**

This step also helps identify some potential processes associated with the requirements.

- User Management: Users must be able to register and log in to the system, with separate roles for students and teachers. The Administrator manages these roles.

- Creation and Assignment of Projects and Tasks: Teachers can create academic projects (i.e., tasks/assignments), defining a title, description, due date, and assigning students to the project.

- Project and Task Management: Teachers can update the project status.

- Project Status Tracking: Each project has a status (e.g., "In Progress," "Completed") that is updated based on task progress. Teachers can update the project status. Students can check the project status.

- Progress and Feedback Updates: Students can record progress on each task and receive feedback from the teacher to ensure they meet the objectives. - Attaching Documents and Files: Students can upload files or links relevant to their assigned projects. Instructors can upload files and links to each project (e.g., guides or related materials).

- Accessibility and Usability: The application must run on a web platform, accessible on both desktop computers and mobile devices. It must be an intuitive platform.

- Security: The platform will store personal data of the people involved (students, instructors, and other academic staff), as well as login credentials according to each assigned role. This data must be adequately protected using data encryption techniques.

- Activity Notifications: The system sends notifications about important updates, such as new comments, assigned tasks, or changes to deadlines.

- Activity History: The application maintains a record of all activities related to each project, so students and instructors can check their progress.

- Visuals: Provide the platform with an intuitive and legible design, with clear and simple fonts, eye-catching icons and buttons, and professional colors.

# Part 3: Requirements Analysis

## **a) Consolidated Requirements List**

Organizing, breaking down, and consolidating the requirements and processes identified during the development and synthesis of the project idea. Functional Requirements (FR) are visualized first, followed by Non-Functional Requirements (NFR).

### Functional Requirements (FR):

**\*Priority associated before performing the MoSCoW classification**

| **ID** | User (comment): Feature                                                                                                                           | Associated Process | **Priority\*** |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | -------------- |
| FR-001 | User (anyone): The User registers in the Application with their information – registration does not grant a role by default.                      | User Management    | High           |
| FR-002 | User (anyone): Log in to the Application with their registered data.                                                                              | User Management    | High           |
| FR-003 | Administrator: Assign Student or Professor roles to the User                                                                                      | User Management    | High           |
| FR-004 | Professor: Create groups (classes) and assign students to these groups for the monitoring or delivery of their projects.                          | User Management    | High           |
| FR-005 | Professor: Create projects (see: tasks or assignments) for a group (class). Include information such as title, description, due date, and status. | Task Management    | High           |
| FR-006 | Professor: Assign projects to specific student(s) in the course in question.                                                                      | Task Management    | Medium         |
| FR-007 | Professor: Update the status of a project according to the progress of the tasks (intermediate deliveries registered).                            | Task Management    | Low            |
| FR-008 | Student: Check the status of an assigned project and its corresponding information.                                                               | Task Management    | High           |
| FR-009 | Student: Register or submit progress (e.g., midterm delivery) on each assigned project, as required.                                              | Task Management    | Medium         |
| FR-010 | Student: Submit a final delivery for an assigned project.                                                                                         | Task Management    | High           |
| FR-011 | Professor: Provide feedback on project submissions made by assigned students; it is given to them.                                                | Task Management    | Medium         |
| FR-012 | Student: Upload files or links relevant to assigned project deliveries.                                                                           | Attachments        | High           |
| FR-013 | Professor: Upload files or links for each project (e.g., guides or materials).                                                                    | Attachments        | High           |
| FR-014 | User (anyone): Upload a profile picture or icon associated with the user in question.                                                             | Attachments        | Low            |
| FR-015 | User (anyone): Check previous progress of assigned activities.                                                                                    | Activity Log       | Low            |
| FR-016 | Student: Check the assigned projects and their identifier.                                                                                        | Task Management    | High           |

### Non-Functional Requirements (NFR):

**\*Priority associated before performing the MoSCoW classification**

| **ID**  | **User (comment): Feature**                                                                                                       | Associated Process          | **Priority\*** |
| ------- | --------------------------------------------------------------------------------------------------------------------------------- | --------------------------- | -------------- |
| NFR-001 | The application must be compatible with mobile devices (smartphones, tablets) and desktop computers (PCs).                        | Accessibility and usability | High           |
| NFR-002 | The application should be intuitive and easy to use.                                                                              | Accessibility and usability | High           |
| NFR-003 | Ensure the protection of personal and/or sensitive data through encryption.                                                       | Security                    | High           |
| NFR-004 | Use secure credentials to prevent security breaches or unauthorized role access.                                                  | Security                    | High           |
| NFR-005 | The application takes less than 5 seconds on standard connection conditions.                                                      | Performance                 | High           |
| NFR-006 | The application must support multiple users without compromising performance.                                                     | Performance                 | Medium         |
| NFR-007 | The Application sends notifications to Users about important updates (e.g., new task, comments, changes in dates, delivery made). | Notifications               | Medium         |
| NFR-008 | The Platform maintains an Activity Log for each project.                                                                          | Activity Log                | Low            |
| NFR-009 | The site design should allow for the future integration of new functionalities without requiring a complete restructuring.        | Scalability                 | Medium         |
| NFR-010 | Clean visual design, with clear typography.                                                                                       | Design                      | Medium         |
| NFR-011 | Professional color palette. Eye-catching icons and buttons.                                                                       | Design                      | Medium         |

## **b) Associated Process identified**

- For Functional Requirements (FR):
  - User Management
  - Task Management
  - Attachments
  - Class management (optional)

- For Non-Functional Requirements (NFR):
  - Accessibility and usability
  - Security
  - Performance
  - Notifications
  - Activity Log
  - Scalability
  - Design

## **c) MoSCoW classification**

The prioritization carried out, both for Functional Requirements (FR) and for Non-Functional Requirements (NFR), can be summarized as follows:

| **Must Have (M)** | **Should Have (S)** | **Could Have (C)** | **Won’t Have (W)** |
| ----------------- | ------------------- | ------------------ | ------------------ |
| FR-001            | FR-004              | FR-006             | FR-014             |
| FR-002            | FR-011              | FR-007             | _NFR-011_          |
| FR-003            | FR-012              | FR-009             |                    |
| FR-005            | FR-013              | FR-015             |                    |
| FR-008            | _NFR-006_           | _NFR-005_          |                    |
| FR-010            |                     | _NFR-007_          |                    |
| FR-016            |                     | _NFR-008_          |                    |
| _NFR-001_         |                     | _NFR-010_          |                    |
| _NFR-002_         |                     |                    |                    |
| _NFR-003_         |                     |                    |                    |
| _NFR-004_         |                     |                    |                    |
| _NFR-009_         |                     |                    |                    |

Certain factors have been taken into account for the classification of functionalities and their effort estimation.

**Available resources:** A team of four university students will act as developers, software architects, UX designers, and testers. The following resources are available, though their limitations vary:

- Time for design, development, and testing: This varies depending on each team member. Factors such as university studies and work outside of university are taken into account.
- Repository: A GitHub repository will be used for this project. With a Pro account, deployment tools are available if needed.
- Cloud storage: Services such as Google Docs or Microsoft 365, accessible through university email, will be used for synchronization and/or collaborative development of various documents. Storage limits vary between 15 and 100 GB, depending on the service. Project development synchronization depends on the GitHub repository.
- External tools: The preferred development software may also vary depending on the developer, and more options may become available later; these may include Visual Studio Code, PyCharm Community Edition, etc. Among the frameworks considered are React and FastAPI. Other supporting tools may include GitHub Copilot Pro and OpenAI ChatGPT.

**Technical complexity:** Given the project's characteristics and needs, as well as the available resources of the development team, three types of tasks have been identified, based on their implementation complexity, regardless of priority:

- Basic Tasks (2 to 5 points)
- Medium Tasks (5 to 8 points)
- Complex Tasks (8 to 13 points)

**Impact on user experience and relationship with project objectives:** Initially, the goal is to build an application capable of performing its core functionalities, prioritized as Must (and Should) in this initial module. Improvements to the user experience are a priority in subsequent functionalities, planned as Should, Could, and Won't.

## **d) Project Scope**

In general, the objective of this project is to provide a functional platform for managing, assigning, tracking, submitting, and providing feedback on projects in an academic setting.

Conceptually, the platform aims to allow users, previously registered on their own, in their student and professor roles, to manage and track assignments and projects within an academic environment.

Within the application, users will be able to log in to the platform and, once logged in, use it according to their assigned roles. These roles are determined by the platform administrator.

Professors will be able to create and manage groups corresponding to their classes or courses, and within these groups, create and manage assignments for that class. Managing classes involves grouping a number of registered students and creating assignments and other updates within the class. Managing assignments involves creating and deleting tasks, as well as assigning them with relevant information and materials; it should also be possible to assign tasks to specific student subgroups and provide feedback for each assignment (or project or task) submission.

Students must be able to review assigned projects, viewing their status and other relevant information. They will also be able to submit intermediate or final deliverables, as needed, and receive feedback from the instructor on each submission.

The limits established in this project module divide the functionalities into two groups: those included in the MVP and those outside the project scope.

The functionalities included in the defined MVP are those classified as Must (M) and Should (S); these ensure that the system is functional for the intended users (students and instructors) in its initial version.

| Module                               | ID      | Functional                                                 | Proceso Asociado            |
| ------------------------------------ | ------- | ---------------------------------------------------------- | --------------------------- |
| User authentication and management   | FR-001  | User sign up                                               | User Management             |
|                                      | FR-002  | Sign in                                                    | User Management             |
|                                      | FR-003  | Role assignment                                            | User Management             |
| Task Management: Project Assignment  | FR-005  | Project creation                                           | Task Management             |
|                                      | FR-008  | Check project status                                       | Task Management             |
|                                      | FR-016  | Check which projects are assigned                          | Task Management             |
|                                      | FR-010  | Final project deliveries                                   | Task Management             |
| Task Management: Project Delivery    | FR-012  | File upload by students                                    | Attachments                 |
|                                      | FR-013  | File upload by professors                                  | Attachments                 |
| Creating classes, feedback recording | FR-004  | Groups (classes) creation                                  | User Management             |
|                                      | FR-011  | Project delivery feedback                                  | Task Management             |
| Usability, optimization and security | NFR-001 | Web cross-platform compatibility                           | Accessibility and usability |
|                                      | NFR-002 | Application usability                                      | Accessibility and usability |
|                                      | NFR-003 | Data protection                                            | Security                    |
|                                      | NFR-004 | Credential security                                        | Security                    |
|                                      | NFR-006 | Support for multiple users without performance degradation | Performance                 |
|                                      | NFR-009 | Modular design                                             | Scalability                 |
