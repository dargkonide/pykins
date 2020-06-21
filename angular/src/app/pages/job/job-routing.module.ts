import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { JobComponent } from './components/job/job.component';
import { HistoryComponent } from './components/history/history.component';
import { BuildComponent } from './components/build/build.component';
import { JobPageComponent } from './job-page.component';

const routes: Routes = [{
  path: '', component: JobPageComponent,
  children: [
    { path: '', redirectTo: 'history' },

    {path: 'history', component: HistoryComponent},
    {path: 'job', component: JobComponent},
    {path: 'build', component: BuildComponent},

    { path: '**', redirectTo: '' },

  ]
 }];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class JobRoutingModule { }
