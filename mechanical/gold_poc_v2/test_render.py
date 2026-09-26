import vtk
r=vtk.vtkSTLReader();r.SetFileName('/workspace/scratch/3c33fd07ed4c/gold_poc_v2/STL/P06_bowl.stl');r.Update()
m=vtk.vtkPolyDataMapper();m.SetInputConnection(r.GetOutputPort());a=vtk.vtkActor();a.SetMapper(m);a.GetProperty().SetColor(.88,.62,.15)
ren=vtk.vtkRenderer();ren.SetBackground(1,1,1);ren.AddActor(a);win=vtk.vtkRenderWindow();win.SetOffScreenRendering(1);win.SetSize(700,600);win.AddRenderer(ren)
ren.ResetCamera();cam=ren.GetActiveCamera();cam.Azimuth(35);cam.Elevation(40);cam.OrthogonalizeViewUp();win.Render();f=vtk.vtkWindowToImageFilter();f.SetInput(win);f.Update();w=vtk.vtkPNGWriter();w.SetFileName('/workspace/scratch/3c33fd07ed4c/gold_poc_v2/assets/test.png');w.SetInputConnection(f.GetOutputPort());w.Write();print('rendered')
