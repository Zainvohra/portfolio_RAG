import { Calendar, Users, Mail, FileText, TrendingUp } from "lucide-react";

interface Action {
  id: string;
  title: string;
  description: string;
  prompt: string;
  icon: React.ReactNode;
  category: string;
}

export const ACTIONS_LIST: Action[] = [
  {
    id: "attendance-report",
    title: "Get Attendance Report",
    description:
      "Generate attendance reports for an employee within a date range",
    prompt:
      "get attendance report for user [user_id] from '[start_date]' till '[end_date]'",
    icon: <Calendar className="w-4 h-4" />,
    category: "Tool Calling",
  },
  {
    id: "onboarding-email",
    title: "Send Onboarding Emails",
    description: "Send welcome and onboarding emails to new employees",
    prompt:
      "send onboarding emails to new employee with employee ID [employee_id]",
    icon: <Mail className="w-4 h-4" />,
    category: "Tool Calling",
  },
  {
    id: "missing-attendance",
    title: "Missing Attendance Report",
    description:
      "Returns a list of users with missing attendance records, violations or leaves",
    prompt:
      "get missing attendance for user [user_id] from '[start_date]' till '[end_date]'",
    icon: <TrendingUp className="w-4 h-4" />,
    category: "Tool Calling",
  },
  {
    id: "employee-handbook",
    title: "Employee Handbook",
    description: "Search and query related to employee handbook",
    prompt: "What's the company policy for leaves?",
    icon: <Users className="w-4 h-4" />,
    category: "RAG",
  },
  {
    id: "self-review",
    title: "Self Review",
    description: "Get answers related to your performance, goals, and feedback",
    prompt:
      "What are my learning goals, is there any common goal which needs to be focused?",
    icon: <FileText className="w-4 h-4" />,
    category: "RAG",
  },
  {
    id: "employee-handbook",
    title: "Employee Handbook",
    description: "Search and query related to employee handbook",
    prompt: "Provide me details about the OPD?",
    icon: <Users className="w-4 h-4" />,
    category: "RAG",
  },
  {
    id: "consolidate-review",
    title: "Consolidated Review",
    description: "Compare and observe the performance across reviews",
    prompt:
      "Which AI tools have I started to use and which tool have I continued using?",
    icon: <FileText className="w-4 h-4" />,
    category: "RAG",
  },
  {
    id: "employee-handbook",
    title: "Employee Handbook",
    description: "Reasoning to validate eligibility as per the policy",
    prompt:
      "I have been working for 2 years, am I eligible for the company car policy? If yes, what is the process to avail it?",
    // prompt: "How can I earn an extra leave? explain in detail",
    icon: <Users className="w-4 h-4" />,
    category: "RAG",
  },
  {
    id: "consolidate-review",
    title: "Consolidated Review",
    description: "Compare and observe the performance across reviews",
    prompt:
      "As a manager, how can I help him to improve his performance? What are the key areas of improvement across reviews?",
    icon: <Users className="w-4 h-4" />,
    category: "RAG",
  },
  {
    id: "self-review",
    title: "Self Review",
    description: "Get answers related to your performance, goals, and feedback",
    prompt:
      "What are my contribution toward the values of the organization in the 2024's review?",
    icon: <FileText className="w-4 h-4" />,
    category: "RAG",
  },
];
