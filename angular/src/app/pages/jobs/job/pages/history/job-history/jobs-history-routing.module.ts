import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from 'src/app/services/auth/AuthGuard';

import { JobHistoryComponent } from './job-history.component';
import { LogsComponent } from './logs/logs.component';
import { VarsComponent } from './vars/vars.component';

const routes: Routes = [
  {
    path: '',
    canActivate: [AuthGuard],
    component: JobHistoryComponent,
    children: [
      { path: '', redirectTo: 'logs' },
      { path: 'logs', canActivate: [AuthGuard], component: LogsComponent },
      { path: 'vars', canActivate: [AuthGuard], component: VarsComponent },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class JobsRoutingModule {}
