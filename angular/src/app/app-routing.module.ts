import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from './pages/login/login.component';
import { AuthGuard } from './services/auth/AuthGuard ';

const routes: Routes = [
  {
    path: '',
    canActivate: [AuthGuard],
    pathMatch: 'full',
    redirectTo: 'jobs',
  },
  {
    path: 'login',
    component: LoginComponent
  },
  {
    path: 'jobs',
    canActivate: [AuthGuard],
    loadChildren: () =>
      import('./pages/jobs/job-list.module').then((m) => m.JobsListModule),
  },
  {
    path: 'hosts',
    canActivate: [AuthGuard],
    loadChildren: () =>
      import('./pages/hosts/hosts.module').then((m) => m.HostsModule),
  },
  {
    path: 'calendar',
    canActivate: [AuthGuard],
    loadChildren: () =>
      import('./pages/calendar/calendar.module').then((m) => m.CalendarModule),
  },
  {
    path: 'jobs/:jobName',
    canActivate: [AuthGuard],
    loadChildren: () =>
      import('./pages/jobs/job/job-page.module').then((m) => m.JobModule),
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
