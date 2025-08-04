import axios from "axios";

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8080";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export interface ChatRequest {
  message: string;
  user_id?: string;
}

export interface ChatResponse {
  response: string;
  status: "success" | "error";
  data?: any;
}

export const chatService = {
  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    try {
      // Convert frontend format to backend format
      const backendRequest = { query: request.message };
      console.log("🚀 Frontend calling:", API_BASE_URL + "/pulse/chat/");
      console.log("�� Sending request:", backendRequest);
      const response = await api.post("/pulse/chat/", backendRequest);
      console.log("📥 Received response:", response.data);
      return { response: response.data, status: "success" };
    } catch (error) {
      console.error("Error sending message:", error);
      throw error;
    }
  },

  async sendOnboardingEmails(userId?: string): Promise<ChatResponse> {
    try {
      const response = await api.post("/tools/send-onboarding-emails", {
        user_id: userId,
      });
      return response.data;
    } catch (error) {
      console.error("Error sending onboarding emails:", error);
      throw error;
    }
  },

  async identifyMissingAttendance(
    maxMissingDays: number,
    minViolations: number
  ): Promise<ChatResponse> {
    try {
      const response = await api.post("/tools/identify-missing-attendance", {
        max_missing_days: maxMissingDays,
        min_violations: minViolations,
      });
      return response.data;
    } catch (error) {
      console.error("Error identifying missing attendance:", error);
      throw error;
    }
  },

  async getAttendanceReport(
    userId: string,
    startDate: string,
    endDate: string
  ): Promise<ChatResponse> {
    try {
      const response = await api.post("/tools/get-attendance-report", {
        user_id: userId,
        start_date: startDate,
        end_date: endDate,
      });
      return response.data;
    } catch (error) {
      console.error("Error getting attendance report:", error);
      throw error;
    }
  },

  async sendLmMeetingNotesReminder(): Promise<ChatResponse> {
    try {
      const response = await api.post("/tools/send-lm-meeting-notes-reminder");
      return response.data;
    } catch (error) {
      console.error("Error sending LM meeting notes reminder:", error);
      throw error;
    }
  },
};

export default api;
