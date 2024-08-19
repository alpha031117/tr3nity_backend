# Tr3nity
This project features a blockchain-based crowdfunding platform tailored for the pharmaceutical sector, incorporating a Decentralized Autonomous Organization (DAO) system.

## Overview
This DAO project is a Blockchain-Based Crowdfunding Platform, developed by [NextJs](https://github.com/leonnloo/tr3nity-web) integrated with [Django-based RESTful API](https://github.com/alpha031117/tr3nity_backend) that serves as the backend for a research publishing platform. It integrates blockchain technology and IPFS (InterPlanetary File System) for secure and decentralized data storage. The voting system allows validators to cast votes on research proposals during the voting phase. Validators can vote either in favor of or against a proposal. To ensure a fair and balanced voting process, each validator is limited in the number of "Yes" votes they can cast within a list of proposals under the same grant.



### Key Features
- **User Roles**
  - **Reseacher**
    - Upload project's proposal to get crowdfunding.
  - **Validator (Governor)**
      - Review the submitted project proposal and cast a vote to approve it for publication.
  - **Contributor**
      - Provides additional funding to support projects.

- **Quadratic Funding System**
  - The funding amount for each project is determined using a quadratic formula. Specifically, the total funding allocated to a project is proportional to the square of the number of unique supporters. This means that projects with broad support from many individuals receive more funding than those with support concentrated from a few.

- **Funding Allocation In Token**
  - The DAO’s funds are distributed based on the quadratic funding calculations. This approach encourages diverse participation and minimizes the influence of large donors, fostering a more democratic and equitable distribution of resources.

## Future Plan
Voting system implemented in with [smart contract deployed](https://github.com/leonnloo/tr3nity-smart-contracts).

## Technologies Used
- Frontend: Next.JS - [Seperate Repository](https://github.com/leonnloo/tr3nity-web)
- Backend: [Django REST Framework](https://www.django-rest-framework.org/)
- Blockchain: [Maschain]([https://docs.maschain.com/](https://www.maschain.com/))
- Decentralized Storage: [IPFS](https://ipfs.tech/)

## How To Run
In order to run the application, please make sure you have created your MasChain test-net account.<br />

MasChain Portal: https://portal-testnet.maschain.com/login<br />
MasChain Documentation: https://docs.maschain.com/

```bash
# 1. Install requirement dependencies
pip install requirements.txt

# 2. Make database migration
py manage.py makemigrations

# 3. Migrate
py manage.py migrate

# 4. Run server
py manage.py runserver
```
Open [http://localhost:8000](http://localhost:8000) with your browser to see the API gateway.
**Please take note that default port is ``8000``.**

## Learn More

To learn more about Django, take a look at the following resources:
- [Django Documentation](https://www.djangoproject.com/) - learn about Django features
- [Django Rest Framework](https://www.django-rest-framework.org/) - learn abount Django Rest API

## Team
1. [AlphaChong](https://github.com/alpha031117)
2. [Doodledaron](https://github.com/doodledaron)
3. [LeonLoo](https://github.com/leonnloo)
