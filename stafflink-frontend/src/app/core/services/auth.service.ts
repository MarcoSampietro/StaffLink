import { Injectable, signal } from '@angular/core';
import { Router } from '@angular/router';

@Injectable({ providedIn: 'root' })
export class AuthService {
  public ruolo = signal<string | null>(null);

  constructor(private router: Router) {}

  loginSuccess(token: string, ruolo: string) {
    localStorage.setItem('access_token', token);
    this.ruolo.set(ruolo);
  }

  logout() {
    localStorage.removeItem('access_token');
    this.ruolo.set(null);
    this.router.navigate(['/login']);
  }
}
