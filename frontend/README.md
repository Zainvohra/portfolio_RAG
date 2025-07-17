# PulseAI Frontend

A modern, responsive React chat interface for the PulseAI intelligent HR assistant.

## Features

- 🎨 **Modern UI/UX**: Beautiful gradient design with smooth animations
- 💬 **Real-time Chat**: Interactive conversation interface with typing indicators
- 📱 **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- ⚡ **Fast Performance**: Optimized React components with TypeScript
- 🔄 **Auto-scroll**: Messages automatically scroll to the latest
- ⌨️ **Keyboard Shortcuts**: Enter to send, Shift+Enter for new line
- 🎯 **Smart Input**: Auto-resizing textarea with character limits

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

### Environment Variables

Create a `.env` file in the frontend directory:

```env
REACT_APP_API_URL=http://localhost:8000
```

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm test` - Launches the test runner
- `npm run build` - Builds the app for production
- `npm run eject` - Ejects from Create React App (one-way operation)

## Project Structure

```
src/
├── components/
│   ├── ChatInterface.tsx    # Main chat interface
│   ├── Header.tsx          # App header with branding
│   └── MessageBubble.tsx   # Individual message component
├── services/
│   └── api.ts             # API service for backend communication
├── App.tsx                # Main app component
├── App.css               # Main styles
└── index.tsx             # App entry point
```

## API Integration

The frontend is designed to work with the FastAPI backend. The API service includes methods for:

- General chat messages (`/chat`)
- Sending onboarding emails (`/tools/send-onboarding-emails`)
- Identifying missing attendance (`/tools/identify-missing-attendance`)
- Getting attendance reports (`/tools/get-attendance-report`)
- Sending LM meeting notes reminders (`/tools/send-lm-meeting-notes-reminder`)

## Demo Features

Currently, the app includes mock responses for demonstration:

- **Onboarding Emails**: "send onboarding emails"
- **Missing Attendance**: "identify missing attendance"
- **Attendance Reports**: "get attendance report from July 15 to July 30"
- **Meeting Notes**: "send meeting notes reminders"

## Styling

The app uses modern CSS with:
- CSS Grid and Flexbox for layouts
- CSS Custom Properties for theming
- Smooth transitions and animations
- Responsive breakpoints
- Custom scrollbar styling

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Deployment

### Build for Production

```bash
npm run build
```

### Deploy to Netlify

1. Connect your repository to Netlify
2. Set build command: `npm run build`
3. Set publish directory: `build`
4. Add environment variables as needed

### Deploy to Vercel

1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel`
3. Follow the prompts

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

This project is part of the AI Developer Camp initiative.
