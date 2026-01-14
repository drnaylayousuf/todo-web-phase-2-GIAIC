// API client for frontend-backend communication

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';

class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  async request(endpoint: string, options: RequestInit = {}) {
    const url = `${this.baseUrl}${endpoint}`;

    // Check for authentication before making requests to protected endpoints
    const protectedEndpoints = ['/tasks/', '/tasks/toggle']; // Add more as needed - note: POST, GET, PUT, DELETE /tasks/ are all protected
    const isProtectedEndpoint = protectedEndpoints.some(ep => endpoint.startsWith(ep));

    if (isProtectedEndpoint) {
      const token = localStorage.getItem('access_token');
      if (!token) {
        throw new Error('Authentication required. Please log in to continue.');
      }
    }

    const config: RequestInit = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    };

    // Add auth token if available
    const token = localStorage.getItem('access_token');
    if (token) {
      (config.headers as Record<string, string>)['Authorization'] = `Bearer ${token}`;
    } else if (isProtectedEndpoint) {
      // Double check - if it's a protected endpoint and no token, throw error
      throw new Error('Authentication required. Please log in to continue.');
    }

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        let errorMessage = `API request failed: ${response.status} ${response.statusText}`;

        // Try to parse the response as JSON, but handle cases where it's HTML
        try {
          const contentType = response.headers.get('content-type');
          if (contentType && contentType.includes('application/json')) {
            const errorData = await response.json();
            errorMessage = errorData.detail || errorMessage;
          } else {
            // If it's not JSON, it might be an HTML error page
            const errorText = await response.text();
            // Check if it's HTML (contains common HTML tags)
            if (errorText.includes('<html') || errorText.includes('<!DOCTYPE')) {
              errorMessage = `Server error occurred (HTML response received). Status: ${response.status}`;
            } else {
              errorMessage = errorText.substring(0, 200) + (errorText.length > 200 ? '...' : ''); // Limit length
            }
          }
        } catch (e) {
          // If parsing fails, use status code and text
          errorMessage = `Request failed with status ${response.status}. Unable to parse error response.`;
        }

        // Check if this is an authentication error
        if (response.status === 401 || errorMessage.includes('Not authenticated') || errorMessage.includes('Could not validate credentials')) {
          // Remove invalid token if authentication fails
          localStorage.removeItem('access_token');
          errorMessage = 'Authentication failed. Please log in again.';
        } else if (response.status === 500 && errorMessage.includes('An error occurred while creating the task')) {
          // Provide more specific error message for task creation errors
          errorMessage = 'Failed to create task. The server might be experiencing issues. Please try again later.';
        } else if (response.status === 404 && errorMessage.includes('Task not found')) {
          // Provide specific error message for task not found
          errorMessage = 'Task not found or you do not have permission to access this task.';
        }

        throw new Error(errorMessage);
      }

      return response.json();
    } catch (error) {
      // Handle network-level errors like "Failed to fetch"
      if (error instanceof TypeError && error.message.includes('fetch')) {
        // Network error - server might be down or unreachable
        throw new Error(`Network error: Could not reach the server at ${this.baseUrl}. Please make sure the backend server is running and accessible. The backend should be running on http://localhost:8000.`);
      }

      // Re-throw other errors
      throw error;
    }
  }

  // Auth methods
  register = (email: string, password: string) => {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  };

  login = (email: string, password: string) => {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  };

  // Task methods
  getTasks = () => {
    return this.request('/tasks/');
  };

  createTask = (title: string, description?: string) => {
    // Only include description in the payload if it's provided
    const payload: any = { title };
    if (description !== undefined && description !== null && description.trim() !== '') {
      payload.description = description;
    }

    return this.request('/tasks/', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  };

  updateTask = (id: number, title?: string, description?: string, completed?: boolean) => {
    return this.request(`/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify({ title, description, completed }),
    });
  };

  toggleTaskCompletion = (id: number) => {
    return this.request(`/tasks/${id}/toggle`, {
      method: 'PATCH',
    });
  };

  deleteTask = (id: number) => {
    return this.request(`/tasks/${id}`, {
      method: 'DELETE',
    });
  };
}

export const apiClient = new ApiClient();
export default ApiClient;