import { Injectable, inject, signal } from '@angular/core'; // <-- Corretto qui (@angular/core)
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

export interface Utente {
  id_utente: string; 
  cognome: string; 
  nome: string; 
  email: string; 
  ruolo: string;
}

export interface StatisticheDashboard {
  rating_medio: number; 
  posti_totali_richiesti: number; 
  steward_confermati: number;
}

@Injectable({ providedIn: 'root' })
export class AdminService {
  private http = inject(HttpClient);
  private apiUrl = 'https://reimagined-robot-5gv6jppxjqp5h76pq-5000.app.github.dev/api/admin';

  private utentiState = signal<Utente[]>([]);
  private statsState = signal<StatisticheDashboard | null>(null);

  public readonly utenti = this.utentiState.asReadonly();
  public readonly statistiche = this.statsState.asReadonly();

  caricaUtenti(): Observable<Utente[]> {
    return this.http.get<Utente[]>(`${this.apiUrl}/utenti`).pipe(
      tap(u => this.utentiState.set(u))
    );
  }

  modificaRuoloUtente(idUtente: string, nuovoRuolo: string): Observable<any> {
    return this.http.put(`${this.apiUrl}/utenti/${idUtente}/ruolo`, { ruolo: nuovoRuolo }).pipe(
      tap(() => {
        // <-- Aggiunta la tipizzazione esplicita (utenti: Utente[]) e (u: Utente) per Strict Mode
        this.utentiState.update((utenti: Utente[]) => 
          utenti.map((u: Utente) => u.id_utente === idUtente ? { ...u, ruolo: nuovoRuolo } : u)
        );
      })
    );
  }

  caricaStatisticheDashboard(idEvento: number): Observable<StatisticheDashboard> {
    return this.http.get<StatisticheDashboard>(`${this.apiUrl}/dashboard/stats/${idEvento}`).pipe(
      tap(stats => this.statsState.set(stats))
    );
  }
}