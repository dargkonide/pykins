import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

const routes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    redirectTo: 'jobs',
    data: {
        title: 'jobs'
    }
},
  { path: 'jobs', loadChildren: () => import('./pages/jobs/jobs.module').then(m => m.JobsModule) },
  { path: 'hosts', loadChildren: () => import('./pages/hosts/hosts.module').then(m => m.HostsModule) },
  { path: 'calendar', loadChildren: () => import('./pages/calendar/calendar.module').then(m => m.CalendarModule) },
  { path: 'jobs/:name', loadChildren: () => import('./pages/job/job.module').then(m => m.JobModule) }

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
