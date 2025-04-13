# StudyRight — Your smarter way to study.

## Inspiration
Did you know?
Let’s be honest — we’ve all been there. Mindlessly doom-scrolling through short-form videos for hours. In fact, the average TikTok user spends around 95 minutes a day on the app — and for many college students, that number climbs to 3–4 hours daily.

And as software engineers or college students, we’ve all had that classic moment: sitting in class thinking, ‘I’ll just study this later.’ Then later comes… and the regret sets in.

That’s where StudyRight comes in. We’ve built a tool that turns your study notes into engaging, AI-generated short videos — tailored for your short attention span. Instead of fighting your content addiction, we’re using it to your advantage.

Learn smarter, not harder — with StudyRight.

## What it does
StudyRight takes lecture notes or study materials provided by the user and uses AI to generate short, visually engaging explainer videos. These videos are designed in the style of popular short-form content, making it easier for students to retain information in a format they’re already addicted to. Users can input their notes, choose a style or topic focus, and get back a digestible, entertaining video that helps them study on the go — whether they’re commuting, procrastinating, or just in need of a quick review.

## How we built it
I built this web application using Flask as the backend framework, MongoDB for storing user and video metadata, and AWS S3 for hosting the generated video content. The app allows users to upload lecture notes, which are processed into educational short-form videos using AI. I used JWT authentication to securely manage user sessions, and the frontend, built with React, communicates with the Flask API to handle file uploads, trigger video generation, and display the final videos. The system is modular, scalable, and leverages cloud storage for efficient video delivery.

## Challenges we ran into
One of the biggest challenges we faced was integrating multiple technologies — from frontend video input to backend AI processing — into a seamless user experience. Converting raw lecture notes into coherent, engaging video scripts required fine-tuning our AI prompt design to get consistent, high-quality outputs. We also ran into issues with video generation speed and file handling, especially when dealing with large media assets and cloud storage through AWS S3. Debugging compatibility between services and ensuring everything ran smoothly across different devices and environments definitely pushed us to think creatively and troubleshoot efficiently.

## Accomplishments that we're proud of
We successfully built a full-stack AI-powered web application that transforms lecture notes into short educational videos. We integrated complex systems like AWS S3 for cloud storage, MongoDB for dynamic data handling, and JWT for secure user authentication. We also implemented a seamless frontend-to-backend flow using React and Flask, and learned how to work with APIs like Gemini for content generation. This project reflects our ability to combine AI, cloud, and web technologies into a working product — from user login to delivering final videos in the browser.

## What we learned
Throughout this project, we learned how to design and build a complete end-to-end web application using modern technologies. We gained hands-on experience with integrating cloud services like AWS S3 for file storage and MongoDB for database management. We learned how to securely manage users with JWT authentication and how to build scalable backend APIs using Flask. On the frontend, we deepened our understanding of React and how to handle file uploads, state management, and UI feedback during asynchronous tasks. Most importantly, we learned how to connect all these tools to work together, and how to troubleshoot and debug real-world integration issues.

## What's next for SitRight
We envision expanding StudyRight into a mobile app, allowing students to learn anywhere, anytime — whether on a commute or in between classes. We also plan to add collaboration and sharing features so study groups can upload notes together and learn from each other’s videos. Additionally, personalized learning paths will use AI to analyze users' habits and content to recommend tailored study videos, helping students focus on what they need most.

## Team
- [Team Member 1] - Frontend Development and UI/UX Design
- [Team Member 2] - Machine Learning
- [Team Member 3] - Backend Development
