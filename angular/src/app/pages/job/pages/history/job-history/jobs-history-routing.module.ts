import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { JobHistoryComponent } from './job-history.component';
import {LogsComponent} from './logs/logs.component';
import { StagesComponent } from './stages/stages.component';
import { VarsComponent } from './vars/vars.component';

const routes: Routes = [{ path: '', component: JobHistoryComponent,
  children: [
    { path: '', redirectTo: 'logs' },
    { path: 'logs', component: LogsComponent },
    { path: 'vars', component: VarsComponent },
    { path: 'stages', component: StagesComponent },
  ]}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class JobsRoutingModule { }
