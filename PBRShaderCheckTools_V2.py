# coding=UTF-8

'''
Quick Assign PBR Map with TDAL specification

2018/12/20 Sai Ling
'''

import mset
import os

# global vars

global_TextureFormatItems = ['.png','.jpg']
global_SurfaceShaderItems = ['None', 'Normals', 'Detail Normals', 'Parallax']
global_MicrosurfaceShaderItems = ['None','Gloss','Roughness','Advanced Micro']
global_AlbedoShaderItems = ['None','Albedo','Vertex Color','Dota Color']
global_DiffusionShaderItems = ['None','Unlit','Lambertian','Microfiber','Subsurface Scatter','Dota Diffuse']
global_ReflectivityShaderItems = ['None','Specular','Metalness','Adv. Metalness','Refractive Index','Dota Specular']
global_ReflectionShaderItems = ['None','Blinn-Phong','GGX','Anisotropic']
global_SecondaryReflectionShaderItems = ['None','Mirror','Blinn-Phong','GGX','Anisotropic',r"Newton's Rings"]
global_OcclusionShaderItems = ['None','Occlusion']
global_EmissiveShaderItems = ['None','Emissive','Heat','Fluorescent']
global_TransparencyShaderItems = ['None','Cutout','Dither','Add','Refraction']
global_ExtraShaderItems = ['None','Substance','Custom']



# mockup marmoset class for easy build 

## drawer 
class Mset_drawer(object):
    '''
    as an template, not use it directly 
    '''
    def __init__(self, title='Rollout',  contained=None, rolloutOpen=True): 
        self.window = mset.UIWindow(name='', register=False)
        self.rollout = mset.UIDrawer()
        self.rollout.title = title
        self.rollout.open = rolloutOpen
        if contained :
            self.rollout.containedControl = contained
        else:
            self.rollout.containedControl = self.window

## double label
class Mset_labelInfo(object):
    '''
    combine label as info
    '''
    def __init__(self,title='label', titlesize=120, info='info', infosize=120):
        self.window = mset.UIWindow(name='', register=False)
        self.window.width = 280
        self.label = mset.UILabel(title + ' : ')
        self.label.fixedWidth = titlesize
        self.info = mset.UILabel(info)
        self.info.fixedWidth = infosize

        self.draw()
    
    def draw(self):
        self.window.addElement(self.label)
        self.window.addElement(self.info)


## open dialog
class Mset_showDialog(object):
    '''
    a open dialog button with textfield
    use string as keyword
    dialogtype: 'OpenFile' , 'OpenFolder' , 'SaveFile'
    '''
    def __init__(self,title='Path:', dialogtype='OpenFolder'):
        self.window = mset.UIWindow(name='', register=False)
        self.window.width = 280
        self.title = mset.UILabel(title)
        self.textField = mset.UITextField()
        self.button = mset.UIButton('....')
        self.button.small = True
        self.dialogtype = dialogtype

        self.draw()
        self.controllers()

    def draw(self):
        self.window.addElement(self.title)
        self.window.addReturn()
        self.window.addElement(self.textField)
        self.window.addElement(self.button)
    
    def controllers(self):
        self.button.onClick = lambda:(self.updatepath())

    def updatepath(self):
        if self.dialogtype == 'OpenFile':
            path = mset.showOpenFileDialog()
            if path != '':
                self.textField.value = path
        if self.dialogtype == 'OpenFolder':
            path = mset.showOpenFolderDialog()
            if path != '':
                self.textField.value = path
        if self.dialogtype == 'SaveFile':
            path = mset.showSaveFileDialog()
            if path != '':
                self.textField.value = path

## listbox
class Mset_listBox(object):
    def __init__(self,title='List', items=['item1','item2']):
        self.window = mset.UIWindow(name='', register=False)
        self.window.width = 280
        self.listBox = mset.UIListBox(title)
        self.items = items

        self.draw()
    def draw(self):
        self.window.addElement(self.listBox)
        for item in self.items:
            self.listBox.addItem(item)
        self.listBox.selectedItem = 0

## affix list
class Mset_affixList(object):
    def __init__(self,mapList=['item1','item2']):
        self.window = mset.UIWindow(name='', register=False)
        self.window.width = 280
        self.rollout = mset.UIDrawer()
        self.rollout.title = 'Assign Material'
        self.rollout.open = True
        self.rollout.containedControl = self.window
        self.affixlist = Mset_listBox(title='Filename Suffix : ',items=['Suffix', 'Infix', 'Prefix'])
        self.extlist = Mset_listBox(title='file ext : ',items=global_TextureFormatItems)
        self.mapListDict = {}
        self.mapList = mapList

        self.draw()
        self.controllers()

    def controllers(self):
        self.affixlist.listBox.onSelect = lambda:(self.draw())

    def draw(self):
        self.window.clearElements()
        self.mapListDict.clear() 
        self.window.addElement(self.affixlist.listBox)
        self.window.addSpace(60)
        self.window.addElement(self.extlist.listBox)
        self.window.addReturn()
        ### create map list field
        for text in self.mapList:
            if text not in self.mapListDict:
                newLabel = mset.UILabel(text)
                newField = mset.UITextField()
                newField.width = 160
                if self.affixlist.listBox.selectedItem == 0:
                    newField.value = ( '_' + text )
                elif self.affixlist.listBox.selectedItem == 1:
                    newField.value = ( '_' + text + '_')
                elif self.affixlist.listBox.selectedItem == 2:
                    newField.value = ( text + '_')
                self.window.addElement(newLabel)
                self.window.addStretchSpace()
                self.mapListDict[text] = newField
                self.window.addElement(newField)
                self.window.addReturn() 

# UI

class UI_AssignMaterial(object):
    def __init__(self,mapList=[]):
        self.window = mset.UIWindow(name='', register=False)
        self.rollout = mset.UIDrawer('Assign Material')
        self.rollout.open = True
        self.rollout.containedControl = self.window
        self.opendialog = Mset_showDialog(title='Select Texture Folder')
        self.btn_assingFromFolder = mset.UIButton( ('Assign From Folder').center(18,' ') )
        self.btn_assingFromSubfolder = mset.UIButton( ('From External Subfolder').center(5,' ') )
        self.affixlist = Mset_affixList(mapList=['Normal', 'Roughness', 'BaseColor', 'Metallic', 'Specular', 'Opacity'])


        self.draw()

        self.controllers()

    def draw(self):
        self.window.addElement(self.opendialog.window)
        self.window.addReturn()
        self.window.addElement(self.btn_assingFromFolder)
        self.window.addStretchSpace()
        self.window.addElement(self.btn_assingFromSubfolder)
        self.window.addReturn()
        self.window.addElement(self.affixlist.window)

    def controllers(self):
        self.btn_assingFromFolder.onClick = Mset_funcs.assignfromfolder
        self.btn_assingFromSubfolder.onClick = Mset_funcs.assignauto

class UI_ChangeShaderType(object):
    def __init__(self):
        self.window = mset.UIWindow(name='', register=False)
        self.rollout = mset.UIDrawer('Set All Material Shader Type')
        self.rollout.open = False
        self.rollout.containedControl = self.window
        self.surface_shader = Mset_listBox(title='Surface : ',items=global_SurfaceShaderItems)
        self.microsurface_shader = Mset_listBox(title='Microsurface : ',items=global_MicrosurfaceShaderItems)
        self.albedo_shader = Mset_listBox(title='Albedo : ',items=global_AlbedoShaderItems)
        self.diffuse_shader = Mset_listBox(title='Diffusion : ',items=global_DiffusionShaderItems)
        self.reflectivity_shader = Mset_listBox(title='Reflectivity : ',items=global_ReflectivityShaderItems)
        self.reflection_shader = Mset_listBox(title='Reflection : ',items=global_ReflectionShaderItems)
        self.secondaryreflection_shader = Mset_listBox(title='Secondary Reflection : ',items=global_SecondaryReflectionShaderItems)
        self.occlusion_shader = Mset_listBox(title='Occlusion : ',items=global_OcclusionShaderItems)
        self.emissive_shader = Mset_listBox(title='Emmisive : ',items=global_EmissiveShaderItems)
        self.transparency_shader = Mset_listBox(title='Transparency : ',items=global_TransparencyShaderItems)
        self.extra_shader = Mset_listBox(title='Extra : ',items=global_ExtraShaderItems)

        ### initoption
        self.surface_shader.listBox.selectedItem = 1
        self.microsurface_shader.listBox.selectedItem = 1
        self.albedo_shader.listBox.selectedItem = 1
        self.diffuse_shader.listBox.selectedItem = 2
        self.reflectivity_shader.listBox.selectedItem = 4
        self.reflection_shader.listBox.selectedItem = 0
        self.secondaryreflection_shader.listBox.selectedItem = 0
        self.occlusion_shader.listBox.selectedItem = 0
        self.emissive_shader.listBox.selectedItem = 0
        self.transparency_shader.listBox.selectedItem = 2
        self.extra_shader.listBox.selectedItem = 0
        
        self.draw()

        self.controllers()

    def draw(self):
        self.window.addElement(self.surface_shader.listBox)
        self.window.addReturn()
        self.window.addElement(self.microsurface_shader.listBox)
        self.window.addReturn()
        self.window.addElement(self.albedo_shader.listBox)
        self.window.addReturn()
        self.window.addElement(self.diffuse_shader.listBox)
        self.window.addReturn()
        self.window.addElement(self.reflectivity_shader.listBox)
        self.window.addReturn()
        self.window.addElement(self.reflection_shader.listBox)
        self.window.addReturn()
        self.window.addElement(self.secondaryreflection_shader.listBox)
        self.window.addReturn()
        self.window.addElement(self.occlusion_shader.listBox)
        self.window.addReturn()
        self.window.addElement(self.emissive_shader.listBox)
        self.window.addReturn()
        self.window.addElement(self.transparency_shader.listBox)
        self.window.addReturn()
        self.window.addElement(self.extra_shader.listBox)
        self.window.addReturn()



    def controllers(self):
        self.surface_shader.listBox.onSelect = lambda: (Mset_funcs.fix_Material(
            'surface', global_SurfaceShaderItems[self.surface_shader.listBox.selectedItem]))
        self.microsurface_shader.listBox.onSelect = lambda: (Mset_funcs.fix_Material(
            'microsurface', global_MicrosurfaceShaderItems[self.microsurface_shader.listBox.selectedItem]))
        self.albedo_shader.listBox.onSelect = lambda: (Mset_funcs.fix_Material(
            'albedo', global_AlbedoShaderItems[self.albedo_shader.listBox.selectedItem]))
        self.diffuse_shader.listBox.onSelect = lambda: (Mset_funcs.fix_Material(
            'diffusion', global_DiffusionShaderItems[self.diffuse_shader.listBox.selectedItem]))
        self.reflectivity_shader.listBox.onSelect = lambda: (Mset_funcs.fix_Material(
            'reflectivity', global_ReflectivityShaderItems[self.reflectivity_shader.listBox.selectedItem]))
        self.reflection_shader.listBox.onSelect = lambda: (Mset_funcs.fix_Material(
            'reflection', global_ReflectionShaderItems[self.reflection_shader.listBox.selectedItem]))
        self.secondaryreflection_shader.listBox.onSelect = lambda: (Mset_funcs.fix_Material(
            'secondaryReflection', global_SecondaryReflectionShaderItems[self.secondaryreflection_shader.listBox.selectedItem]))
        self.occlusion_shader.listBox.onSelect = lambda: (Mset_funcs.fix_Material(
            'occlusion', global_OcclusionShaderItems[self.occlusion_shader.listBox.selectedItem]))
        self.emissive_shader.listBox.onSelect = lambda: (Mset_funcs.fix_Material(
            'emissive', global_EmissiveShaderItems[self.emissive_shader.listBox.selectedItem]))
        self.transparency_shader.listBox.onSelect = lambda: (Mset_funcs.fix_Material(
            'transparency', global_TransparencyShaderItems[self.transparency_shader.listBox.selectedItem]))
        self.extra_shader.listBox.onSelect = lambda: (Mset_funcs.fix_Material(
            'extra', global_ExtraShaderItems[self.extra_shader.listBox.selectedItem]))

class UI_SceneInfo(object):
    def __init__(self):
        self.window = mset.UIWindow(name='', register=False)
        self.rollout = mset.UIDrawer('Scene Info')
        self.rollout.open = False
        self.rollout.containedControl = self.window
        self.btn_refresh = mset.UIButton(('Refresh').center(80, ' '))
        self.btn_refresh.small = True
        self.object_counts = Mset_labelInfo(title='Object Count')
        self.material_counts = Mset_labelInfo(title='Materials Counts')
        self.trianglefaces = Mset_labelInfo(title='Triangle Faces Count')

        self.draw()

        self.controllers()
    
    def draw(self):
        self.window.addElement(self.btn_refresh)
        self.window.addReturn()
        self.window.addElement(self.object_counts.window)
        self.window.addReturn()
        self.window.addElement(self.material_counts.window)
        self.window.addReturn()
        self.window.addElement(self.trianglefaces.window)

    def controllers(self):
        self.btn_refresh.onClick = self.refreshinfo

    def refreshinfo(self):
        objects = mset.getAllObjects()
        polycount = 0
        for obj in objects:
            try:
                polycount += len(obj.mesh.triangles)
            except:
                polycount += 0
        
        self.trianglefaces.info.text = '{:20,d}'.format(polycount)
        self.material_counts.info.text = str(len(mset.getAllMaterials())) 
        self.object_counts.info.text = str(len(objects)) 


class UI_GltfExporter(object):
    def __init__(self):
        #### main window
        self.window = mset.UIWindow(name='', register=False)
        self.window.width = 280
        self.rollout = mset.UIDrawer('glTF Exporter')
        self.rollout.open = True
        self.rollout.containedControl = self.window

        #### single mode
        self.singlemode_window = mset.UIWindow(name='', register=False)
        self.singlemode_window.width = 280   
        self.singlemode_rollout = mset.UIDrawer('Single Mode')
        self.singlemode_rollout.containedControl = self.singlemode_window
        self.singlemode_rollout.open = False
        self.singlemode_rollout.setMinor(False)

        self.dialog_signleexport = Mset_showDialog(title='Export .glb file', dialogtype='SaveFile' )
        self.btn_export = mset.UIButton( ('Export to Specific Path').center(68, ' ') )
        self.chk_savescene = mset.UICheckBox()
        self.chk_savescene.label = ' Save Scene File'
        #### batch mode
        self.batchmode_window = mset.UIWindow(name='', register=False)
        self.batchmode_window.width = 280   
        self.batchmode_rollout = mset.UIDrawer('Batch Mode')
        self.batchmode_rollout.containedControl = self.batchmode_window
        self.batchmode_rollout.open = True
        self.batchmode_rollout.setMinor(True)

        self.dialog_batchimport = Mset_showDialog(title='Batch import from folder', dialogtype='OpenFolder' )
        self.dialog_batchexoprt = Mset_showDialog(title='Batch export to folder', dialogtype='OpenFolder' )
        self.search_subfolder = mset.UICheckBox()
        self.search_subfolder.label = ' Serach subfolders'
        self.export_subfolder = mset.UICheckBox()
        self.export_subfolder.label = ' Export to External Relate path'
        self.btn_batchexport = mset.UIButton( ('Batch Export').center(72, ' ') )
        self.chk_savescenes = mset.UICheckBox()
        self.chk_savescenes.label = ' Save Scene File'

        #### settings
        self.setting_window = mset.UIWindow(name='', register=False)
        self.setting_window.width = 280 
        self.setting_rollout = mset.UIDrawer('glTF Exporter Setting')
        self.setting_rollout.open = True
        self.setting_rollout.containedControl = self.setting_window

        self.label_setting = mset.UILabel( (' glTF Exoprt Quality Setting ').center(52, '-') )
        self.quality = Mset_listBox(title='Texture Quality : ',items=['Low','Medium','High','Full'])
        self.vertexcolor = mset.UICheckBox()
        self.vertexcolor.label = 'Use Vertex Colors'
        self.matelliclabel = mset.UILabel('Metaliness Threshold : ')
        self.matellic = mset.UISliderFloat() 

        ### initoption
        self.matellic.value = 0.8

        self.draw()

        self.controllers()
    
    def draw(self):
        self.window.clearElements()

        self.singlemode_window.addElement(self.dialog_signleexport.window)
        self.singlemode_window.addReturn()
        self.singlemode_window.addElement(self.btn_export)
        self.singlemode_window.addReturn()
        self.singlemode_window.addElement(self.chk_savescene)
        self.singlemode_window.addReturn()

        self.batchmode_window.addElement(self.dialog_batchimport.window)
        self.batchmode_window.addReturn()
        self.batchmode_window.addElement(self.dialog_batchexoprt.window)
        self.batchmode_window.addReturn()
        self.batchmode_window.addElement(self.search_subfolder)
        self.batchmode_window.addReturn()
        self.batchmode_window.addElement(self.export_subfolder)
        self.batchmode_window.addReturn()
        self.batchmode_window.addElement(self.chk_savescenes)
        self.batchmode_window.addReturn()
        self.batchmode_window.addElement(self.btn_batchexport)
        
        
        self.setting_window.clearElements()
        self.setting_window.addElement(self.label_setting)
        self.setting_window.addReturn()
        self.setting_window.addElement(self.quality.listBox)
        self.setting_window.addStretchSpace()
        self.setting_window.addElement(self.vertexcolor)
        self.setting_window.addReturn()
        self.setting_window.addElement(self.matelliclabel)
        self.setting_window.addElement(self.matellic)

        self.window.addElement(self.singlemode_rollout)
        self.window.addReturn()
        self.window.addElement(self.batchmode_rollout)
        self.window.addReturn()
        self.window.addElement(self.setting_rollout)
        self.window.addReturn()

    def controllers(self):
        self.singlemode_rollout.onOpenClose = self.switch_single
        self.batchmode_rollout.onOpenClose = self.switch_batch
        self.btn_export.onClick = Mset_funcs.export_Glb_single
        self.btn_batchexport.onClick = Mset_funcs.export_Glb_batch

    def switch_single(self):
        self.batchmode_rollout.open = not self.singlemode_rollout.open
        self.batchmode_rollout.setMinor(self.batchmode_rollout.open)

    def switch_batch(self):
        self.singlemode_rollout.open = not self.batchmode_rollout.open
        self.singlemode_rollout.setMinor(self.singlemode_rollout.open)

    def export_batch(self):
        textureQuality = self.quality.listBox.selectedItem
        metalnessTh = self.matellic.value
        externalFiles = []
        objects = mset.getAllObjects()

        fbxfiles = []

        batchimportpath = self.dialog_batchimport.textField.value
        batchexportpath = self.dialog_batchexoprt.textField.value
        
        for obj in objects:
            if type(obj) == mset.ExternalObject :
                externalFiles.append(obj)
                obj.visible = False

            # mset.exportGLTF(path=batchexportpath, quality=textureQuality, metalnessThreshold=metalnessTh)
        
        print ('export_batch')

## functions 

class Mset_funcs(object):

    @classmethod
    def fix_Material(cls,subroutines,shadertype):
        Materials = mset.getAllMaterials()
        for Material in Materials:
            Material.setSubroutine(subroutines,shadertype)
            # print (shadertype)

    @classmethod
    def collect_Files(cls,filenameExt,searchPath='', patterns=[],depth=1):
        if depth == 0:
            depth = 90
        collection = []
        if searchPath !='':
            searchdepth = searchPath.count(os.path.sep) + depth
            for dirpath, dirnames, filenames in os.walk(searchPath):
                dirdepth=(dirpath.count(os.path.sep))
                if dirdepth < searchdepth :
                    for filename in filenames:
                        if filename.endswith(filenameExt):
                            for pattern in patterns:
                                if pattern in filename:
                                    collection.append(os.path.join(dirpath,filename))

        return (collection)

    @classmethod
    def assignfromfolder(cls):
        tempPath = AssignMaterial.opendialog.textField.value
        cls.assign_TDALmaps(tempPath,1)

    @classmethod
    def assignauto(cls):
        externalFiles = [obj for obj in mset.getAllObjects() if type(obj) == mset.ExternalObject ]
        
        for externalFile in externalFiles:
            tempPath = os.path.dirname(externalFile.path)
            print (tempPath)
            cls.assign_TDALmaps(tempPath,0)

    @classmethod
    def assign_TDALmaps(cls,folderpath,searchdepth):
        cls.inital_TDALMaterials()
        tempPath = folderpath
        tempExt = global_TextureFormatItems[AssignMaterial.affixlist.extlist.listBox.selectedItem]
        mapListDict = AssignMaterial.affixlist.mapListDict
        tempPattern = [ v.value for v in AssignMaterial.affixlist.mapListDict.values()]

        if tempPath != '':
            texturefiles = cls.collect_Files(filenameExt=tempExt, searchPath=tempPath,  patterns=tempPattern, depth=searchdepth)
            materials = mset.getAllMaterials()
            for material in materials:
                normalmap = material.name + AssignMaterial.affixlist.mapListDict['Normal'].value
                roughnessmap = material.name + AssignMaterial.affixlist.mapListDict['Roughness'].value
                albedomap = material.name + AssignMaterial.affixlist.mapListDict['BaseColor'].value
                metallicmap = material.name + AssignMaterial.affixlist.mapListDict['Metallic'].value
                specularmap = material.name + AssignMaterial.affixlist.mapListDict['Specular'].value
                opacitymap = material.name + AssignMaterial.affixlist.mapListDict['Opacity'].value

                for texturefile in texturefiles:
                    if normalmap in os.path.basename(texturefile):
                        Mset_material.assign_SurfaceShader_Normals(material,texturefile)
                    if roughnessmap in os.path.basename(texturefile):
                        Mset_material.assign_MicroSurfaceShader_Gloss(material,texturefile)
                    if albedomap in os.path.basename(texturefile):
                        Mset_material.assign_AlbedoShader(material,texturefile)
                    if opacitymap in os.path.basename(texturefile):
                        Mset_material.assign_TransparencyShader_Cutout(material,texturefile)
                    if metallicmap in os.path.basename(texturefile):
                        Mset_material.assign_ReflectivityShader_AdvMetalness_Metalness(material,texturefile)
                    if specularmap in os.path.basename(texturefile):
                        Mset_material.assign_ReflectivityShader_AdvMetalness_Specular(material,texturefile)      

    @classmethod
    def inital_TDALMaterials(cls):
        for material in mset.getAllMaterials():
            material.setSubroutine('surface','Normals')
            material.setSubroutine('microsurface','Gloss')
            material.setSubroutine('albedo','Albedo')
            material.setSubroutine('diffusion','Lambertian')
            material.setSubroutine('reflectivity','Adv. Metalness')
            material.setSubroutine('reflection','GGX')
            material.setSubroutine('emissive','None')
            material.setSubroutine('transparency','None')


    @classmethod
    def inital_PBRMaterials(cls):
        for material in mset.getAllMaterials():
            material.setSubroutine('surface','Normals')
            material.setSubroutine('microsurface','Gloss')
            material.setSubroutine('albedo','Albedo')
            material.setSubroutine('diffusion','Lambertian')
            material.setSubroutine('reflectivity','Adv. Metalness')
            material.setSubroutine('transparency','Cutout')

    @classmethod
    def export_Glb_batch(cls):
     
        importfolder = GltfExporter.dialog_batchimport.textField.value
        exportfolder = GltfExporter.dialog_batchexoprt.textField.value
        searchdepth = 1
        savescenes = GltfExporter.chk_savescenes.value

        if GltfExporter.search_subfolder.value == True:
            searchdepth = 0
        
        fbxfiles = cls.collect_Files('.fbx',searchPath = importfolder,patterns=['.fbx'],depth=searchdepth)

        for fbxfile in fbxfiles:
            sceneObjName = (os.path.basename(fbxfile)).split('.')[0]
            searchpath = os.path.dirname(fbxfile)
            mset.newScene()
            Externalfbx = mset.ExternalObject()
            Externalfbx.path = fbxfile
            Externalfbx.name = sceneObjName

            cls.assign_TDALmaps(searchpath,0)

            if savescenes:
                mset.saveScene(exportfolder + sceneObjName + '.tbscene')

            Mset_funcs.export_MakeScreenShot(exportfolder + sceneObjName)
            cls.export_Glb(exportfolder + sceneObjName + '.glb')

    
    
    @classmethod
    def export_Glb_single(cls):
        exportPath = GltfExporter.dialog_signleexport.textField.value
        if GltfExporter.chk_savescene.value:
            mset.saveScene(os.path.splitext(exportPath)[0] + '.tbscene')
        cls.export_Glb(exportPath)
    
    @classmethod
    def export_Glb(cls,exportPath):
        exportfolder = os.path.dirname(exportPath)
        textureQuality = GltfExporter.quality.listBox.selectedItem
        metalnessTh = GltfExporter.matellic.value        

        if os.path.exists(exportfolder):
            screenshotpath = (os.path.splitext(exportPath))[0]
            Mset_funcs.export_MakeScreenShot(screenshotpath)
            mset.exportGLTF(path=exportPath, quality=textureQuality, metalnessThreshold=metalnessTh)
            print ("export %s success" % (exportPath)   )           



    @classmethod
    def export_MakeScreenShot(cls,screenshotpath):
        skyfile = r'C:\Program Files\Marmoset\Toolbag 3\data\sky\Indoor Fluorescents.tbsky'
        savepath = screenshotpath + '.jpg'
        if os.path.isfile(skyfile):
            skyobj = mset.findObject('Sky')
            skyobj.loadSky(skyfile)

            camera = mset.findObject('Main Camera')
            camera.position = [70, 30, 105]
            camera.rotation = [0, 33.5, 0.0]
            mset.frameScene()
            mset.exportScreenshot(
                path=savepath, 
                width=839, 
                height=416, 
                sampling=8, 
                transparency=False)
    
    @classmethod
    def TDALGlb(cls):
        skyfile = r'C:\Program Files\Marmoset\Toolbag 3\data\sky\Indoor Fluorescents.tbsky'
        # exportpath = r'O:\201808_H3D_extension\300models\glb\\' 
        importpath = (r'O:\201808_H3D_extension\300models\OutputForGlb')
        retargetpath = (r'O:\201808_H3D_extension\300models\Output')
        fbxfiles = []
        for dirpath, dnames, fnames in os.walk(importpath):
            for f in fnames:
                if f.endswith(".fbx"):
                    fbxfiles.append(os.path.join(dirpath,f))
        
        # print (fbxfiles)

        for fbxfile in fbxfiles:

            templist = fbxfile.split('\\' )[:-2]
            temppath = "\\".join(templist)

            sceneObjName = (templist[len(templist)-1])
            newoutput = temppath.replace(importpath,retargetpath)

            # exportpath = 

            scene = mset.newScene()
            skyobj = mset.findObject('Sky')
            skyobj.loadSky(skyfile)
            mycam = mset.findObject('Main Camera')
            # mycam.position = [120, 30, 120]
            mycam.position = [70, 30, 105]
            mycam.rotation = [0, 33.5, 0.0]

            Externalfbx = mset.ExternalObject()
            Externalfbx.path = fbxfile
            Externalfbx.name = sceneObjName
            mset.frameScene()
            screenShotPath = newoutput + '.jpg'

            mset.exportScreenshot(path=screenShotPath, width=839, height=416, sampling=8, transparency=False)
            
            # export glb
            glbpath = newoutput + '.glb'
            if os.path.exists(newoutput):
                mset.exportGLTF(path=glbpath, quality=1, metalnessThreshold=0.8)
                print ("export %s success" % (glbpath) )

    @classmethod
    def test(cls):
        fbxfiles = []
        scenename = []
        importpath = (r'C:\temp\Output')
        retargetpath = (r'O:\201808_H3D_extension\300models\Output')
        for dirpath, dnames, fnames in os.walk(importpath):
            for f in fnames:
                if f.endswith(".fbx"):
                    fbxfile = os.path.join(dirpath,f)

                    templist = fbxfile.split('\\' )[:-2]
                    temppath = "\\".join(templist)

                    scenename = (templist[len(templist)-1])
                    newoutput = temppath.replace(importpath,retargetpath)
                    fbxfiles.append(fbxfile)  
                    print (fbxfile, scenename, newoutput)
class Mset_material(object):
    '''
    class for TDAL material template  
    '''
    def __init__(self):
        pass

    '''
    SurfaceShader
    '''
    @classmethod
    def assign_SurfaceShader_Normals(cls,material,map1):
        material.setSubroutine('surface','Normals')
        if os.path.isfile(map1):
            myTexture = mset.Texture(path=map1)
            myTexture.sRGB=False
            myTexture.useMipmaps=True
            material.getSubroutine('surface').setField('Normal Map',myTexture)

        material.getSubroutine('surface').setField('Flip Y',True)

    @classmethod
    def assign_SurfaceShader_Detail_Normals(cls,material,map1,map2):
        material.setSubroutine('surface','Detail Normals')
        if os.path.isfile(map1):
            myTexture = mset.Texture(path=map1)
            myTexture.sRGB=False
            myTexture.useMipmaps=True
            material.getSubroutine('surface').setField('Normal Map',myTexture)
 
        if os.path.isfile(map2):
            myTexture = mset.Texture(path=map2)
            myTexture.sRGB=False
            myTexture.useMipmaps=True
            material.getSubroutine('surface').setField('Detail Normal Map',myTexture)

        material.getSubroutine('surface').setField('Flip Y',True)

    '''
    MicroSurfaceShader
    '''
    @classmethod
    def assign_MicroSurfaceShader_Gloss(cls,material,map1):
        material.setSubroutine('microsurface','Gloss')
        if os.path.isfile(map1):
            myTexture = mset.Texture(path=map1)
            myTexture.sRGB=False
            myTexture.useMipmaps=True
            material.getSubroutine('microsurface').setField('Gloss Map',myTexture)

        material.getSubroutine('microsurface').setField('Invert',True)


    @classmethod
    def assign_MicroSurfaceShader_Roughness(cls,material,map1):
        material.setSubroutine('microsurface','Roughness')
        if os.path.isfile(map1):
            myTexture = mset.Texture(path=map1)
            myTexture.sRGB=False
            myTexture.useMipmaps=True
            material.getSubroutine('microsurface').setField('Roughness Map',myTexture)

        material.getSubroutine('microsurface').setField('Roughness', 1)

    '''
    AlbedoShader
    '''
    @classmethod
    def assign_AlbedoShader(cls,material,map1):
        material.setSubroutine('albedo','Albedo')
        if os.path.isfile(map1):
            myTexture = mset.Texture(path=map1)
            myTexture.sRGB=True
            myTexture.useMipmaps=True
            material.getSubroutine('albedo').setField('Albedo Map',myTexture)
            material.getSubroutine('albedo').setField('Color',[255,255,255])

    @classmethod
    def assign_DiffusionShader(cls,material):
        material.setSubroutine('diffusion','Lambertian')
    
    '''
    ReflectivityShader
    '''
    @classmethod
    def assign_ReflectivityShader_AdvMetalness_Metalness(cls,material,map1):
        material.setSubroutine('reflectivity','Adv. Metalness')
        if os.path.isfile(map1):
            myTexture = mset.Texture(path=map1)
            myTexture.sRGB=False
            myTexture.useMipmaps=True
            material.getSubroutine('reflectivity').setField('Metalness Map',myTexture)

    @classmethod
    def assign_ReflectivityShader_AdvMetalness_Specular(cls,material,map1):
        material.setSubroutine('reflectivity','Adv. Metalness')
        if os.path.isfile(map1): 
            myTexture = mset.Texture(path=map1)
            myTexture.sRGB=False
            myTexture.useMipmaps=True
            material.getSubroutine('reflectivity').setField('Specular Level Map',myTexture)


    '''
    TransparencyShader
    '''
    @classmethod
    def assign_TransparencyShader_Cutout(cls,material,map1):
        material.setSubroutine('transparency','Cutout')
        if os.path.isfile(map1): 
            myTexture = mset.Texture(path=map1)
            myTexture.sRGB=False
            myTexture.useMipmaps=True
            material.getSubroutine('transparency').setField('Alpha Map',myTexture) 
        
        material.getSubroutine('transparency').setField('Channel',4)
 
    @classmethod
    def assign_TransparencyShader_Dither(cls,material,map1):
        material.setSubroutine('transparency','Dither')
        if os.path.isfile(map1): 
            myTexture = mset.Texture(path=map1)
            myTexture.sRGB=False
            myTexture.useMipmaps=True
            material.getSubroutine('transparency').setField('Alpha Map',myTexture) 



## create ui class
AssignMaterial = UI_AssignMaterial()
GltfExporter = UI_GltfExporter()
ChangeShaderType = UI_ChangeShaderType()
SceneInfo = UI_SceneInfo()



# Main window
mainWindow = mset.UIWindow('Moonshine TDAL Tools')
mainWindow.width = 305

## add ui to Main window
mainWindow.addReturn()
mainWindow.addElement(AssignMaterial.rollout)
mainWindow.addReturn()
mainWindow.addElement(GltfExporter.rollout)
mainWindow.addReturn()
mainWindow.addElement(ChangeShaderType.rollout)
mainWindow.addReturn()
mainWindow.addElement(SceneInfo.rollout)
mainWindow.addReturn()

closebutton = mset.UIButton( ('Close Window').center(76,' ') )
closebutton.onClick = lambda:(mset.shutdownPlugin())
mainWindow.addElement(closebutton)
## showUI
mainWindow.visible = True
