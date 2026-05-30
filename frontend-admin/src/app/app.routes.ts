import { Routes } from '@angular/router';
import { roleGuard } from './core/guards/role.guard';

export const routes: Routes = [
  { path: 'login', loadComponent: () => import('./features/auth/login/login.component').then(c => c.LoginComponent) },
  { path: 'dashboard-organizzatore', loadComponent: () => import('./features/organizer/dashboard/dashboard.component').then(c => c.DashboardComponent), canActivate: [roleGuard(['organizzatore', 'admin'])] },
  { path: 'admin-panel', loadComponent: () => import('./features/admin/users-manager/users-manager.component').then(c => c.UsersManagerComponent), canActivate: [roleGuard(['admin'])] },
  { path: '', redirectTo: 'login', pathMatch: 'full' }
];
