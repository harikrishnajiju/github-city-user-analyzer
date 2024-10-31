# github-city-user-analyzer
***
# GitHub User and Repository Analysis

This project utilizes the GitHub API to scrape and analyze users based in Basel with over 10 followers and their repositories.

## Key Highlights
- This analysis focuses on users from the city of Basel, providing insights into their activities and connections on GitHub.
- The data includes users' follower counts, the number of repositories, and their hireable status.
- The project also explores the relationship between user characteristics and their repositories.

## Data Sources
- **users.csv**: Contains user data for GitHub users located in Basel with more than 10 followers. The data includes:
  - `login`: User's GitHub ID
  - `name`: Full name of the user
  - `company`: Company they work at (cleaned)
  - `location`: City of the user
  - `email`: User's email address
  - `hireable`: Whether they are open to being hired
  - `bio`: Short bio of the user
  - `public_repos`: Number of public repositories
  - `followers`: Number of followers
  - `following`: Number of people they are following
  - `created_at`: Date of joining GitHub

- **repositories.csv**: Contains repository data for the users listed in users.csv, with details including:
  - `login`: User's GitHub ID
  - `full_name`: Full name of the repository
  - `created_at`: Date of repository creation
  - `stargazers_count`: Number of stars
  - `watchers_count`: Number of watchers
  - `language`: Programming language used
  - `has_projects`: Whether projects are enabled
  - `has_wiki`: Whether wiki is enabled
  - `license_name`: License name of the repository

## Analysis Overview
- Users were analyzed based on their follower counts, repositories, and whether they are hireable.
- Key findings include:
  - Top 5 users with the most followers
  - The most common licenses used in repositories
  - Analysis of programming languages preferred by users

## Recommendations
- Developers should consider increasing their public repositories to potentially enhance their follower counts.
- Hireable users may benefit from optimizing their profiles, including having a public email and an engaging bio.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>

