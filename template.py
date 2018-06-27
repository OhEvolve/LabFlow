
class Template(object):

    traits = ['type','shape','sequence','concentration','length']

    def __init__(self,*args,**kwargs):

        self.no_input       = False
        self.type           = None
        self.shape          = None
        self.sequence       = None
        self.concentration  = None
        self.length         = None

        self.update(*args,**kwargs) 

    def update(self,*args,**kwargs):
        """ Updates class attributes using dict args and kwargs """
        for arg in args + (kwargs,):
            for k,v in arg.items():
                setattr(self, k, v)
    
    def __eq__(self,template):
        """ Checks if all specified attributes are equivalent """
        if not isinstance(template,Template):
            return False
        
        # if this are no origin templates (i.e. distributor of oligos)
        if self.no_input == True or template.no_input == True:
            if self.no_input == True and template.no_input == True: 
                return True
            else:                                                   
                return False

        # matches each relavent trait
        for trait in self.traits:
            if getattr(self,trait) == getattr(template,trait): continue
            if getattr(self,trait) == None:                    continue
            if getattr(template,trait) == None:                continue
            return False
        return True

    def __repr__(self):
        """ Representation of template """

        if self.no_input == True: return '*'

        _type,_shape,_seq,_conc,_len = '','','','',''
        if self.type:          _type  = self.type
        if self.shape:         _shape = '{} '.format(self.shape)
        if self.sequence:      _seq   = ', with sequence {}'.format(self.sequence)
        if self.concentration: _conc  = ' of {} concentration'.format(self.concentration)
        if self.length:        _len   = ', {}'.format(self.length)
        return _shape + _type + _seq + _conc + _len

            
        




