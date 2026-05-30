import { Injectable, signal, computed } from '@angular/core';

interface AuthState {
  token: string | null;
  ruolo: 'admin' | 'organizzatore' | 'steward' | null;
  isAuthenticated: boolean;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private state = signal<AuthState>({
    token: localStorage.getItem('jwt_token'),
    ruolo: localStorage.getItem('user_role') as any,
    isAuthenticated: !!localStorage.getItem('jwt_token')
  });

  public readonly token = computed(() => this.state().token);
  public readonly ruolo = computed(() => this.state().ruolo);
  public readonly isAuthenticated = computed(() => this.state().isAuthenticated);

  loginSuccess(token: string, ruolo: any) {
    localStorage.setItem('jwt_token', token);
    localStorage.setItem('user_role', ruolo);
    this.state.set({ token, ruolo, isAuthenticated: true });
  }

  logout() {
    localStorage.removeItem('jwt_token');
    localStorage.removeItem('user_role');
    this.state.set({ token: null, ruolo: null, isAuthenticated: false });
  }
}
