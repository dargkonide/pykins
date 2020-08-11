import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { JobHistoryComponent } from './job-history.component';
import {LogsComponent} from './logs/logs.component';

const routes: Routes = [{ path: '', component: JobHistoryComponent,
  children: [
    { path: '', redirectTo: 'logs' },
    { path: 'logs', component: LogsComponent },
  ]}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class JobsRoutingModule { }
