import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StewardService } from '../../../core/services/steward.service';

@Component({
  selector: 'app-steward-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './steward-dashboard.component.html'
})
export class StewardDashboardComponent implements OnInit {
  public stewardService = inject(StewardService);
  ngOnInit() { this.stewardService.caricaTurni().subscribe(); }
  accettaTurno(id_turno: number) { 
    this.stewardService.accettaTurno(id_turno).subscribe(); 
  }
}
