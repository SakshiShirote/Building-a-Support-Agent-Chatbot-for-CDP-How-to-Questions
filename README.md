# Building-a-Support-Agent-Chatbot-for-CDP-How-to-Questions
## Overview

This project is a chatbot designed to assist users with "how-to" questions related to four Customer Data Platforms (CDPs): Segment, mParticle, Lytics, and Zeotap. The chatbot retrieves relevant information from the official documentation of these CDPs to guide users in performing tasks within each platform.

## Features

### 1. Answer "How-to" Questions

The chatbot understands and responds to user questions about performing specific tasks within Segment, mParticle, Lytics, and Zeotap.

Example questions:
-"How do I set up a new source in Segment?"
-"How can I create a user profile in mParticle?"
-"How do I build an audience segment in Lytics?"
-"How can I integrate my data with Zeotap?"

### 2. Extract Information from Documentation

-Retrieves relevant information from official documentation and provides step-by-step instructions.
-Handles multiple queries and variations in phrasing.

### 3. Cross-CDP Comparisons (Bonus Feature)

-Provides comparisons between different CDPs.
-Example: "How does Segment's audience creation process compare to Lytics'?"

## Tech Stack

-Backend: Flask (Python)
-Frontend: HTML, CSS, JavaScript
-Parsing: BeautifulSoup (for potential document scraping)
-Regex: Used for platform and query extraction
-API: JSON-based communication between frontend and backend
