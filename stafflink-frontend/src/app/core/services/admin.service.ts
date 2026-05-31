import { Injectable, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class AdminService {
  private http = inject(HttpClient);
  private baseUrl = `${environment.backendUrl}/api/admin`;

  public utenti = signal<any[]>([]);
  public statistiche = signal<any>(null);

  caricaUtenti() {
    return this.http.get<any[]>(`${this.baseUrl}/utenti`).pipe(
      tap(dati => this.utenti.set(dati))
    );
  }

  modificaRuoloUtente(id_utente: string, nuovo_ruolo: string) {
    return this.http.put(`${this.baseUrl}/utenti/${id_utente}/ruolo`, { ruolo: nuovo_ruolo }).pipe(
      tap(() => this.caricaUtenti().subscribe())
    );
  }

  caricaStatisticheDashboard(id_evento: number) {
    return this.http.get<any>(`${this.baseUrl}/dashboard/stats/${id_evento}`).pipe(
      tap(stats => this.statistiche.set(stats))
    );
  }
}
