import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { HistoryComponent } from './components/history/history.component';
import { BuildComponent } from './components/build/build.component';
import { JobPageComponent } from './job-page.component';
import {JobService} from "./service/job.service";
import {CodeComponent} from "./components/job/code/code.component";

const routes: Routes = [{
  path: '', component: JobPageComponent,
  children: [
    { path: '', redirectTo: 'history' },

    {path: 'history', component: HistoryComponent},
    {path: 'job', loadChildren: () => import('./components/job/job.module').then(m => m.JobModule), canActivate: [JobService] },
    {path: 'build', component: BuildComponent},

    { path: '**', redirectTo: '' },

  ]
 }];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class JobRoutingModule { }
