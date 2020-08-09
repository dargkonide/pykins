import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { HistoryComponent } from './pages/history/history.component';
import { BuildComponent } from './pages/build/build.component';
import { JobPageComponent } from './job-page.component';
import {JobService} from "./service/job.service";

const routes: Routes = [{
  path: '', component: JobPageComponent,
  children: [
    { path: '', redirectTo: 'history' },

    {path: 'history', component: HistoryComponent},
    {path: 'job', loadChildren: () => import('./pages/job/job.module').then(m => m.JobModule), canActivate: [JobService] },
    {path: 'build', component: BuildComponent},

    { path: '**', redirectTo: '' },

  ]
 }];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class JobRoutingModule { }
