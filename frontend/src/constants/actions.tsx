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
      id: 'attendance-report',
      title: 'Get Attendance Report',
      description: 'Generate attendance reports for an employee within a date range',
      prompt: "get attendance report for user [user_id] from '[start_date]' till '[end_date]'",
      icon: <Calendar className="w-4 h-4" />,
      category: 'Tool Calling'
    },
    {
      id: 'onboarding-email',
      title: 'Send Onboarding Emails',
      description: 'Send welcome and onboarding emails to new employees',
      prompt: "send onboarding emails to new employee with employee ID [employee_id]",
      icon: <Mail className="w-4 h-4" />,
      category: 'Tool Calling'
    },
    {
      id: 'missing-attendance',
      title: 'Missing Attendance Report',
      description: 'Returns a list of users with missing attendance records, violations or leaves',
      prompt: "get missing attendance for user [user_id] from '[start_date]' till '[end_date]'",
      icon: <TrendingUp className="w-4 h-4" />,
      category: 'Tool Calling'
    },
    {
      id: 'employee-handbook',
      title: 'Employee Handbook',
      description: 'Search and query related to employee handbook',
      prompt: "e.g. 'What is the referral bonus policy?'",
      icon: <Users className="w-4 h-4" />,
      category: 'RAG'
    },
    {
      id: 'self-review',
      title: 'Self Review',
      description: 'Get answers related to your performance, goals, and feedback',
      prompt: "e.g. 'What are my goals for this review period?'",
      icon: <FileText className="w-4 h-4" />,
      category: 'RAG'
    }
  ];