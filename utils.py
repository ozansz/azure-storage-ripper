get_container_names = lambda bs: [bc.name for bc in bs.list_containers().items]
get_blob_names_for_container = lambda bs, bc: [bb.name for bb in bs.list_blobs(bc).items] 
