# Quiz Application

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

A robust, Excel-based quiz management system designed for educational institutions. This application streamlines the process of creating, administering, and evaluating quizzes while maintaining comprehensive performance records.

</div>

## 📋 Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Login_Credentials](#login-credentials)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [Data Management](#data-management)
- [Security Considerations](#security-considerations)
- [Contributing](#contributing)
- [License](#license)

## 📖 Overview

The Quiz Application is a comprehensive solution for educational institutions seeking to digitize their assessment process. Built with Python and utilizing Excel for data persistence, it offers a perfect balance between simplicity and functionality.

### Core Capabilities
- Multi-user role management (Teachers/Students)
- Dynamic quiz creation and management
- Real-time performance tracking
- Comprehensive leaderboard system
- Excel-based data persistence

## ✨ Key Features

### 👨‍🏫 Teacher Dashboard
- **Quiz Management**
  - Create and customize quizzes
  - Add multiple-choice questions
  - Set time limits and scoring rules
  - Delete or modify existing quizzes
- **Performance Analytics**
  - View detailed student performance metrics
  - Access comprehensive leaderboard data
  - Generate performance reports

### 👨‍🎓 Student Interface
- **Quiz Taking**
  - Access available quizzes
  - Real-time quiz completion
  - Immediate score feedback
- **Performance Tracking**
  - View personal quiz history
  - Track progress over time
  - Compare performance with peers

## 🔐 Login Credentials

### Teacher Login
- **Username**: `teacher`
- **Password**: `1234`
- **Access**: Teacher Dashboard
- **Features**:
  - Quiz Management (create, customize, delete quizzes)
  - Add multiple-choice questions
  - Set time limits and scoring rules
  - View student performance metrics
  - Access leaderboard data
  - Generate performance reports

### Student Login
- **Username**: `student`
- **Password**: `1234`
- **Access**: Student Interface
- **Features**:
  - Take available quizzes
  - Get immediate score feedback
  - View personal quiz history
  - Track progress
  - Compare performance with peers

## 🏗 System Architecture

### Database Structure
The application utilizes a modular Excel-based storage system:

| File | Purpose | Key Components |
|------|---------|----------------|
| `users.xlsx` | User Management | User profiles, roles, credentials |
| `quizzes.xlsx` | Quiz Repository | Quiz metadata, configurations |
| `questions.xlsx` | Question Bank | Questions, options, correct answers |
| `leaderboard.xlsx` | Performance Tracking | Scores, timestamps, rankings |

### Technical Stack
- **Backend**: `Python 3.x`
- **Data Storage**: Excel (openpyxl)
- **File Structure**: Modular, maintainable architecture

## 🚀 Installation

### Prerequisites
- `Python 3.x`
- pip (Python package manager)

### Setup Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/sabbirahmad12/quiz-application.git
   cd quiz-application
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```bash
   python excel_db.py
   ```

4. Launch the application:
   ```bash
   python main.py
   ```

## 📊 Data Management

### Database Schema

#### Users Table
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Unique identifier |
| username | String | User login name |
| password | String | Encrypted password |
| role | String | User role (teacher/student) |

#### Quizzes Table
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Quiz identifier |
| title | String | Quiz name |
| description | String | Quiz description |

#### Questions Table
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Question identifier |
| quiz_id | Integer | Associated quiz |
| question_text | String | Question content |
| options | Array | Multiple choice options |
| correct_answer | Integer | Correct option index |

#### Leaderboard Table
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Record identifier |
| user_id | Integer | Student identifier |
| quiz_id | Integer | Quiz identifier |
| score | Float | Achieved score |
| time_taken | Integer | Completion time |

## 🔒 Security Considerations

### Current Implementation
- Basic file-based authentication
- Role-based access control
- Excel file data storage

### Recommended Enhancements
- Implement password hashing
- Add session management
- Enable database encryption
- Integrate secure authentication
- Regular security audits
- Backup and recovery procedures

## 🤝 Contributing

We welcome contributions to enhance the Quiz Application. Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Write comprehensive tests
- Update documentation
- Maintain backward compatibility

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
Made with ❤️ for education
</div> 
