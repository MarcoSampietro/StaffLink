import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AdminService } from '../../../core/services/admin.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div style="padding: 20px;">
      <h1>Dashboard Evento</h1>
      @if (adminService.statistiche(); as stats) {
        <div style="display: flex; gap: 20px;">
          <div style="padding: 20px; background: #f8f9fa; border-radius: 10px;">
            <h3>Copertura Personale</h3>
            <h2>{{ stats.steward_confermati }} / {{ stats.posti_totali_richiesti }}</h2>
          </div>
          <div style="padding: 20px; background: #f8f9fa; border-radius: 10px;">
            <h3>Rating Medio</h3>
            <h2>⭐ {{ stats.rating_medio }}</h2>
          </div>
        </div>
      } @else { <p>Caricamento statistiche...</p> }
    </div>
  `
})
export class DashboardComponent implements OnInit {
  public adminService = inject(AdminService);
  ngOnInit() { this.adminService.caricaStatisticheDashboard(1).subscribe(); }
}
