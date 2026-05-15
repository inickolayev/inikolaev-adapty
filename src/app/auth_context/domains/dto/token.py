from dddesign.structure.domains.dto import DataTransferObject


class TokenPairDTO(DataTransferObject):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class RefreshRequestDTO(DataTransferObject):
    refresh_token: str
