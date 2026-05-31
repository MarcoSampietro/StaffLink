import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Router } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';
import { environment } from '../../../../environments/environments';


@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './login.component.html'
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

    this.http.post<any>(`${environment.keycloakUrl}/realms/stafflink-arena/protocol/openid-connect/token`, body.toString(), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }).subscribe({
      next: (res) => {
        const payload = JSON.parse(atob(res.access_token.split('.')[1]));
        const ruolo = payload.realm_access?.roles.includes('admin') ? 'admin' : payload.realm_access?.roles.includes('organizzatore') ? 'organizzatore' : 'steward';
        this.authService.loginSuccess(res.access_token, ruolo);

        this.http.post(`${environment.backendUrl}/api/auth/sync`, {}).subscribe(() => {
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
