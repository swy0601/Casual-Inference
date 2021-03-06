/**
	 * Handle sending notifications needed for natural-id after saving
	 *
	 * @param generatedId The generated entity identifier
	 */
	public void handleNaturalIdPostSaveNotifications(Serializable generatedId) {
		if ( isEarlyInsert() ) {
			// with early insert, we still need to add a local (transactional) natural id cross-reference
			getSession().getPersistenceContext().getNaturalIdHelper().manageLocalNaturalIdCrossReference(
					getPersister(),
					generatedId,
					state,
					null,
					CachedNaturalIdValueSource.INSERT
			);
		}
		// after save, we need to manage the shared cache entries
		getSession().getPersistenceContext().getNaturalIdHelper().manageSharedNaturalIdCrossReference(
				getPersister(),
				getId(),
				state,
				null,
				CachedNaturalIdValueSource.INSERT
		);
	}