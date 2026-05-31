import { Routes } from '@angular/router';
import { HomeComponent } from './features/public/home/home.component';
import { LoginComponent } from './features/auth/login/login.component';
import { UsersManagerComponent } from './features/admin/users-manager/users-manager.component';
import { DashboardComponent } from './features/admin/dashboard/dashboard.component';
import { StewardDashboardComponent } from './features/steward/steward-dashboard/steward-dashboard.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'login', component: LoginComponent },
  { path: 'users-manager', component: UsersManagerComponent },
  { path: 'admin-panel', component: DashboardComponent },
  { path: 'dashboard-organizzatore', component: DashboardComponent },
  { path: 'steward-panel', component: StewardDashboardComponent },
  { path: '**', redirectTo: '' }
];
