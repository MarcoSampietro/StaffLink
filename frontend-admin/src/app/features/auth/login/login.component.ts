import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Router } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <div style="max-width: 400px; margin: 100px auto; padding: 20px; border: 1px solid #ccc; border-radius: 8px;">
      <h2>Accesso StaffLink Arena</h2>
      <form [formGroup]="loginForm" (ngSubmit)="onSubmit()">
        <div style="margin-bottom: 15px;">
          <label>Username</label>
          <input type="text" formControlName="username" style="width: 100%; padding: 8px;">
        </div>
        <div style="margin-bottom: 15px;">
          <label>Password</label>
          <input type="password" formControlName="password" style="width: 100%; padding: 8px;">
        </div>
        @if (errore) { <p style="color: red;">Credenziali non valide.</p> }
        <button type="submit" [disabled]="loginForm.invalid || inCaricamento" style="width: 100%; padding: 10px; background: #0056b3; color: white;">
          {{ inCaricamento ? 'Accesso in corso...' : 'Entra' }}
        </button>
      </form>
    </div>
  `
})
export class LoginComponent {
  private fb = inject(FormBuilder);
  private http = inject(HttpClient);
  private authService = inject(AuthService);
  private router = inject(Router);

  loginForm = this.fb.group({ username: ['', Validators.required], password: ['', Validators.required] });
  errore = false; inCaricamento = false;

  onSubmit() {
    if (this.loginForm.invalid) return;
    this.inCaricamento = true; this.errore = false;
    const { username, password } = this.loginForm.value;

    const body = new HttpParams().set('client_id', 'stafflink-frontend').set('username', username!).set('password', password!).set('grant_type', 'password');

    this.http.post<any>('https://reimagined-robot-5gv6jppxjqp5h76pq-8080.app.github.dev/realms/stafflink-arena/protocol/openid-connect/token', body.toString(), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }).subscribe({
      next: (res) => {
        const payload = JSON.parse(atob(res.access_token.split('.')[1]));
        const ruolo = payload.realm_access?.roles.includes('admin') ? 'admin' : payload.realm_access?.roles.includes('organizzatore') ? 'organizzatore' : 'steward';
        this.authService.loginSuccess(res.access_token, ruolo);

        this.http.post('https://reimagined-robot-5gv6jppxjqp5h76pq-5000.app.github.dev/api/auth/sync', {}).subscribe(() => {
          this.inCaricamento = false;
          if (ruolo === 'admin') this.router.navigate(['/admin-panel']);
          else if (ruolo === 'organizzatore') this.router.navigate(['/dashboard-organizzatore']);
          else { alert('Accesso negato.'); this.authService.logout(); }
        });
      },
      error: () => { this.errore = true; this.inCaricamento = false; }
    });
  }
}
