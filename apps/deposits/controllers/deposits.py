import uuid
from fastapi import HTTPException, status


from apps.deposits.schema.deposits import (
    DepositSchema,
    GetDepositsQuerySchema,
    GetDepositResponseSchema,
    GetDepositsResponseSchema,
    CreateDepositRequestSchema,
    CreateDepositResponseSchema,
    UpdateDepositRequestSchema,
    UpdateDepositResponseSchema
)


async def get_deposit(
    deposit_id: uuid.UUID,
    deposit_repository
) -> GetDepositResponseSchema:
    deposit = await deposit_repository.get_by_id(deposit_id)
    if not deposit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Deposit with id '{deposit_id}' not found",
        )

    return GetDepositResponseSchema(deposit=DepositSchema.model_validate(deposit))


async def get_deposits(
    user_id,
    query: GetDepositsQuerySchema,
    deposit_repository
) -> GetDepositsResponseSchema:
    deposits = await deposit_repository.filter(query.deposit.id)
    return GetDepositResponseSchema()


async def create_deposit(
    user_id: str,
    request: CreateDepositRequestSchema,
    deposit_repository
):
    deposit = await deposit_repository.create(request.model_dump())
    return CreateDepositResponseSchema(deposit=DepositSchema.model_validate(deposit))


async def update_deposit(
    deposit_id: str,
    request: UpdateDepositRequestSchema,
    deposit_repository
):
    deposit = await deposit_repository.update(deposit_id, request.model_dump(exclude_unset=True))
    return UpdateDepositResponseSchema(deposit=DepositSchema.model_validate(deposit))


async def delete_deposit(deposit_id: uuid.UUID, deposit_repository):
    await deposit_repository.delete(deposit_id)



