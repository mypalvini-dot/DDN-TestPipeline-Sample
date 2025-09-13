from .base_vendor import BaseVendor
from .dell_emc import DellEMCVendor
from .netapp import NetAppVendor
from .hpe import HPEVendor
from .generic import GenericVendor

__all__ = [
    'BaseVendor',
    'DellEMCVendor',
    'NetAppVendor',
    'HPEVendor',
    'GenericVendor'
]

VENDOR_MAP = {
    'dell_emc': DellEMCVendor,
    'netapp': NetAppVendor,
    'hpe': HPEVendor,
    'generic': GenericVendor
}

def get_vendor_class(vendor_type: str):
    """Get vendor class by type"""
    return VENDOR_MAP.get(vendor_type.lower(), GenericVendor)
